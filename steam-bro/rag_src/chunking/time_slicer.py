from datetime import timedelta
class TimeSlicer:
    def __init__(self , gap_minutes=30) -> None:
        self.gap_minutes = timedelta(minutes=gap_minutes)


    def slice(self, data: list):
        if not data:return "Bro nv manchi vaadiki kaadhu"
        slices = []
        current_slice = [data[0]]
        for i in range(1 , len(data)):
            prev_time = data[i-1][2]
            curr_time = data[i][2]
            time_diff = curr_time - prev_time
            if time_diff <= self.gap_minutes:
                current_slice.append(data[i])
            else:
                slices.append(current_slice)
                current_slice = [data[i]]
        if current_slice: slices.append(current_slice)
        return slices
    def slice_to_strings(self, data: list):
        slices = self.slice(data)
        slice_strings = []
        for slice in slices:
            combined_text = " ".join([message[1] for message in slice])
            slice_strings.append(combined_text)
        return slice_strings