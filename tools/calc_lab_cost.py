from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Dict, List, Optional


BOOKING = "Booking"
COMPLAINT = "Complaint"
GUIDE = "Guide"
VISA = "Visa"
WEATHER = "Weather"
INFO_INTENTS = (GUIDE, VISA, WEATHER)
ALL_INTENTS = (GUIDE, VISA, WEATHER, BOOKING, COMPLAINT)


@dataclass(frozen=True)
class ModelPricing:
    name: str
    input_per_m: float
    output_per_m: float


@dataclass(frozen=True)
class HistoryStrategy:
    kind: str
    turns: Optional[int] = None
    summary_tokens: int = 150


@dataclass(frozen=True)
class ClassifierStrategy:
    kind: str
    model: Optional[ModelPricing] = None
    input_tokens: int = 150
    output_tokens: int = 20


@dataclass(frozen=True)
class Config:
    name: str
    response_models: Dict[str, ModelPricing]
    classifier: ClassifierStrategy
    history: HistoryStrategy
    web_mode: str
    web_intents: frozenset[str] = field(default_factory=frozenset)
    web_turns_by_intent: Dict[str, List[int]] = field(default_factory=dict)

    def model_for_intent(self, intent: str) -> ModelPricing:
        if intent in self.response_models:
            return self.response_models[intent]
        if "default" in self.response_models:
            return self.response_models["default"]
        raise KeyError(f"No response model configured for intent {intent}")

    def web_turns(self, intent: str, total_turns: int) -> List[int]:
        if self.web_mode == "off":
            return []
        if self.web_mode == "broad":
            return list(range(1, total_turns + 1))
        if intent not in self.web_intents:
            return []
        return [turn for turn in self.web_turns_by_intent.get(intent, []) if 1 <= turn <= total_turns]


@dataclass(frozen=True)
class Scenario:
    name: str
    turns: int
    conv_per_day: int
    days_per_month: int
    intent_mix: Dict[str, float]


@dataclass(frozen=True)
class LabConstants:
    system_prompt_tokens: int = 500
    user_message_tokens: int = 80
    assistant_response_tokens: int = 180
    history_turn_tokens: int = 260
    rag_tokens: int = 1250
    web_search_tokens: int = 800
    web_search_api_cost: float = 0.005
    human_cost_per_conversation: float = 0.50


MODELS = {
    "gpt-4o-mini": ModelPricing("GPT-4o-mini", 0.15, 0.60),
    "gemini-flash-lite": ModelPricing("Gemini 2.5 Flash-Lite", 0.10, 0.40),
    "gemini-flash": ModelPricing("Gemini 2.5 Flash", 0.30, 2.50),
    "deepseek-v4-pro": ModelPricing("DeepSeek V4 Pro", 1.74, 3.48),
    "claude-haiku-4.5": ModelPricing("Claude Haiku 4.5", 1.00, 5.00),
    "gpt-5.5": ModelPricing("GPT-5.5", 5.00, 30.00),
}


PRESET_CONFIGS = {
    "budget-bot": Config(
        name="Budget Bot",
        response_models={"default": MODELS["gpt-4o-mini"]},
        classifier=ClassifierStrategy(kind="keyword"),
        history=HistoryStrategy(kind="last_n", turns=3),
        web_mode="off",
    ),
    "premium-concierge": Config(
        name="Premium Concierge",
        response_models={"default": MODELS["gpt-5.5"]},
        classifier=ClassifierStrategy(kind="llm", model=MODELS["claude-haiku-4.5"]),
        history=HistoryStrategy(kind="full"),
        web_mode="broad",
    ),
    "smart-mix": Config(
        name="Smart Mix",
        response_models={
            GUIDE: MODELS["gemini-flash"],
            WEATHER: MODELS["gemini-flash"],
            VISA: MODELS["deepseek-v4-pro"],
        },
        classifier=ClassifierStrategy(kind="keyword"),
        history=HistoryStrategy(kind="last_n", turns=5),
        web_mode="selective",
        web_intents=frozenset({VISA, WEATHER}),
        web_turns_by_intent={
            VISA: [1, 2],
            WEATHER: [1],
        },
    ),
}


SCENARIOS = {
    "A": Scenario(
        name="Scenario A",
        turns=4,
        conv_per_day=300,
        days_per_month=30,
        intent_mix={
            GUIDE: 0.50,
            VISA: 0.25,
            WEATHER: 0.10,
            BOOKING: 0.10,
            COMPLAINT: 0.05,
        },
    ),
    "B": Scenario(
        name="Scenario B",
        turns=7,
        conv_per_day=1200,
        days_per_month=30,
        intent_mix={
            GUIDE: 0.30,
            VISA: 0.15,
            WEATHER: 0.10,
            BOOKING: 0.35,
            COMPLAINT: 0.10,
        },
    ),
}


def model_cost(model: ModelPricing, input_tokens: int, output_tokens: int) -> float:
    input_cost = input_tokens * model.input_per_m / 1_000_000
    output_cost = output_tokens * model.output_per_m / 1_000_000
    return input_cost + output_cost


def classifier_cost(strategy: ClassifierStrategy) -> float:
    if strategy.kind == "keyword":
        return 0.0
    if strategy.kind == "llm" and strategy.model is not None:
        return model_cost(strategy.model, strategy.input_tokens, strategy.output_tokens)
    raise ValueError(f"Unsupported classifier strategy: {strategy}")


def history_tokens(strategy: HistoryStrategy, turn_number: int, constants: LabConstants) -> int:
    prior_turns = max(turn_number - 1, 0)
    if strategy.kind == "full":
        return prior_turns * constants.history_turn_tokens
    if strategy.kind == "last_n":
        return min(prior_turns, strategy.turns or 0) * constants.history_turn_tokens
    if strategy.kind == "summary":
        if prior_turns == 0:
            return 0
        return strategy.summary_tokens
    raise ValueError(f"Unsupported history strategy: {strategy}")


def turn_cost(config: Config, intent: str, turn_number: int, total_turns: int, constants: LabConstants) -> float:
    model = config.model_for_intent(intent)
    use_web = turn_number in config.web_turns(intent, total_turns)
    input_tokens = (
        constants.system_prompt_tokens
        + history_tokens(config.history, turn_number, constants)
        + constants.rag_tokens
        + constants.user_message_tokens
        + (constants.web_search_tokens if use_web else 0)
    )
    total = model_cost(model, input_tokens, constants.assistant_response_tokens)
    if use_web:
        total += constants.web_search_api_cost
    total += classifier_cost(config.classifier)
    return total


def conversation_cost(config: Config, intent: str, scenario: Scenario, constants: LabConstants) -> float:
    if intent in (BOOKING, COMPLAINT):
        return classifier_cost(config.classifier)
    return sum(turn_cost(config, intent, turn, scenario.turns, constants) for turn in range(1, scenario.turns + 1))


def weighted_average_cost(config: Config, scenario: Scenario, constants: LabConstants) -> float:
    total = 0.0
    for intent, weight in scenario.intent_mix.items():
        total += weight * conversation_cost(config, intent, scenario, constants)
    return total


def monthly_cost(avg_cost: float, scenario: Scenario) -> float:
    return avg_cost * scenario.conv_per_day * scenario.days_per_month


def human_monthly_cost(constants: LabConstants, scenario: Scenario) -> float:
    return constants.human_cost_per_conversation * scenario.conv_per_day * scenario.days_per_month


def savings_pct(ai_monthly: float, human_monthly: float) -> float:
    return (human_monthly - ai_monthly) / human_monthly * 100


def cheaper_than_human_x(ai_monthly: float, human_monthly: float) -> float:
    return human_monthly / ai_monthly if ai_monthly else float("inf")


def render_markdown(selected: List[Config], constants: LabConstants) -> str:
    lines: List[str] = []
    lines.append("| Config | Scenario | Avg Cost/Conv | Monthly Cost | Human Monthly | Cheaper Than Human | Savings % |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for config in selected:
        for scenario in (SCENARIOS["A"], SCENARIOS["B"]):
            avg = weighted_average_cost(config, scenario, constants)
            monthly = monthly_cost(avg, scenario)
            human = human_monthly_cost(constants, scenario)
            lines.append(
                f"| {config.name} | {scenario.name} | ${avg:.5f} | ${monthly:,.2f} | ${human:,.2f} | "
                f"{cheaper_than_human_x(monthly, human):.2f}x | {savings_pct(monthly, human):.2f}% |"
            )
    return "\n".join(lines)


def render_detail(config: Config, constants: LabConstants) -> str:
    lines: List[str] = [f"# {config.name}"]
    for scenario in (SCENARIOS["A"], SCENARIOS["B"]):
        lines.append(f"\n## {scenario.name}")
        for intent in ALL_INTENTS:
            cost = conversation_cost(config, intent, scenario, constants)
            lines.append(f"- {intent}: ${cost:.5f} per conversation")
        avg = weighted_average_cost(config, scenario, constants)
        monthly = monthly_cost(avg, scenario)
        human = human_monthly_cost(constants, scenario)
        lines.append(f"- Weighted average: ${avg:.5f}")
        lines.append(f"- Monthly AI cost: ${monthly:,.2f}")
        lines.append(f"- Human monthly baseline: ${human:,.2f}")
        lines.append(f"- Savings: {savings_pct(monthly, human):.2f}%")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate AI chatbot conversation economics for the Day 27 lab."
    )
    parser.add_argument(
        "--configs",
        nargs="+",
        default=list(PRESET_CONFIGS.keys()),
        choices=list(PRESET_CONFIGS.keys()),
        help="Preset configs to evaluate.",
    )
    parser.add_argument(
        "--web-cost",
        type=float,
        default=0.005,
        help="Web search API cost per call. Default matches worksheet assumptions.",
    )
    parser.add_argument(
        "--detail",
        action="store_true",
        help="Also print per-intent details for each selected config.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    constants = LabConstants(web_search_api_cost=args.web_cost)
    selected = [PRESET_CONFIGS[key] for key in args.configs]
    print(render_markdown(selected, constants))
    if args.detail:
        for config in selected:
            print()
            print(render_detail(config, constants))


if __name__ == "__main__":
    main()
