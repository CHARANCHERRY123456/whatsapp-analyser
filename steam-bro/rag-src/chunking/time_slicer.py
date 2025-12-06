from datetime import timedelta
class TimeSlicer:
    def __init__(self , gap_minutes=30) -> None:
        self.gap_minutes = timedelta(minutes=gap_minutes)


    def slice(self, messages: list):
        if not messages:return "Bro nv manchi vaadiki kaadhu"
        slices = []
        current_slice = [messages[0]]
        for i in range(1 , len(messages)):
            prev_time = messages[i-1][2]
            curr_time = messages[i][2]
            time_diff = curr_time - prev_time
            if time_diff <= self.gap_minutes:
                current_slice.append(messages[i])
            else:
                slices.append(current_slice)
                current_slice = [messages[i]]
        if current_slice: slices.append(current_slice)
        return slices
    