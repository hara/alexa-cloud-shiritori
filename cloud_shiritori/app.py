from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model.ui import SimpleCard

SKILL_NAME = 'クラウドしりとり'

sb = SkillBuilder()


def last_character(term):
    if term[-1] != 'ー':
        return term[-1]
    else:
        return last_character(term[0:-1])


@sb.request_handler(can_handle_func=is_request_type('LaunchRequest'))
def launch_request_handler(handler_input):
    # Handler for Launch Intent
    term = 'エススリー'
    last_of_term = last_character(term)
    speech_text = (f'{SKILL_NAME}へようこそ。クラウド用語に関するしりとりをしましょう。'
                   '私がこれから言うクラウド用語に続けてくださいね。'
                   f'最初の用語は{term}です。{term}の{last_of_term}で始まるクラウド用語を答えてください。')

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME,
                   speech_text)).set_should_end_session(False).response


@sb.request_handler(can_handle_func=is_intent_name('ReplyIntent'))
def reply_intent_handler(handler_input):
    # Handler for Reply Intent
    term = handler_input.request_envelope.request.intent.slots['term'].value
    last_of_term = last_character(term)
    reply = 'トランスクライブ'
    last_of_reply = last_character(reply)
    speech_text = (f'{term}ですね。{term}の{last_of_term}に続くクラウド用語は{reply}です。'
                   f'{reply}の{last_of_reply}で始まるクラウド用語を答えてください。')

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME,
                   speech_text)).set_should_end_session(False).response


@sb.request_handler(can_handle_func=is_intent_name('AMAZON.HelpIntent'))
def help_intent_handler(handler_input):
    # Handler for Help Intent
    speech_text = 'You can say hello to me!'

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).response


@sb.request_handler(
    can_handle_func=
    lambda input: is_intent_name('AMAZON.CancelIntent')(input) or is_intent_name('AMAZON.StopIntent')(input)
)
def cancel_and_stop_intent_handler(handler_input):
    # Single handler for Cancel and Stop Intent
    speech_text = 'Goodbye!'

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name('AMAZON.FallbackIntent'))
def fallback_handler(handler_input):
    # AMAZON.FallbackIntent is only available in en-US locale.
    # This handler will not be triggered except in that locale,
    # so it is safe to deploy on any locale
    speech = ("The Hello World skill can't help you with that.  "
              'You can say hello!!')
    reprompt = 'You can say hello!!'
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type('SessionEndedRequest'))
def session_ended_request_handler(handler_input):
    # Handler for Session End
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # Catch all exception handler, log exception and
    # respond with custom message
    print('Encountered following exception: {}'.format(exception))

    speech = 'Sorry, there was some problem. Please try again!!'
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


lambda_handler = sb.lambda_handler()
