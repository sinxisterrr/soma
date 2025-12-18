from soma_logger import log_processing_pipeline, soma_logger

# At end of /api/process endpoint, add:
log_processing_pipeline(
    user_id=user_id,
    message=message,
    soma_before=initial_soma_state,  # Capture before processing
    soma_after=soma,
    stimuli_input=stimuli,
    stimuli_response=response_stimuli,
    temperature=temperature,
    ai_response=ai_response
)