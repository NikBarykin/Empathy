from agent import Agent


def load_from_file(filename: str):
    result = dict()
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if not line:
                continue

            agent = Agent.deserialize(line)
            result[agent.user_id] = agent

    return result;
