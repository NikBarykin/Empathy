from agent import Agent


def find_match(agent: Agent, agents):
    rate = lambda obj: rate_match(agent, obj)

    best_match = max(
            agents,
            key=rate)

    return (best_match if rate(best_match) > 0
            else None)

def rate_match(subj: Agent, obj: Agent) -> float:
    if (obj.user_id == subj.user_id
        or obj.gender == subj.gender
        or obj.user_id in subj.dislike_ids
        or obj.user_id in subj.like_ids
        ):
        return -1 # we don't want to date oursubj or someone with the same gender

    return 6 - abs(subj.age - obj.age)
