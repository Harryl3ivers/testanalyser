from dataclasses import dataclass

@dataclass
class TestResults:
    name:str
    status:str
    patterns: str
    duration:float
    retries:str
    error_message:str
    run_id:str
    time_stamp:str