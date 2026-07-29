from langgraph.router import route_question

def planner_agent(question):
    route = route_question(question)
    return {
        "route": route,
        "question": question
    }