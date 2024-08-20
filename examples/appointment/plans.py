from examples.appointment.ontology import *


def forget_and_put_appointment_slot_filling_on_agenda(state):
    state.facts = []
    state.resolved_questions = []
    state.agenda = plans[CreateAppointment] + state.agenda


def plan_actions_depending_on_meeting_whole_day(state: DialogState):
    if PredicateProposition(meeting_whole_day, True) in state.facts:
        state.agenda.insert(
            0, PerformAction(CreateWholeDayMeeting, [meeting_person, meeting_date],
                             on_deny=lambda: forget_and_put_appointment_slot_filling_on_agenda(state)))
    else:
        state.agenda = [
            Findout(WhQuestion(meeting_time)),
            PerformAction(CreateNotWholeDayMeeting, [meeting_person, meeting_date, meeting_time],
                          on_deny=lambda: forget_and_put_appointment_slot_filling_on_agenda(state))
        ] + state.agenda


plans = {
    CreateAppointment: [
        Findout(WhQuestion(meeting_person)),
        Findout(WhQuestion(meeting_date)),
        Findout(BooleanQuestion(meeting_whole_day)),
        ExecuteFunction(plan_actions_depending_on_meeting_whole_day)
    ]
}
