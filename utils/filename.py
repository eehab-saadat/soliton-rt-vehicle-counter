from datetime import datetime
def getName(source: str):
    source = source.split("\\")[-1]
    if "http" in source or "https" in source:
        source = source.removeprefix("http://").removeprefix("https://").replace(".com","").replace("www.", "").replace("/", "_").replace(".", "_"). replace(":", "_")
    elif source.isdigit():
        source = f"cam{source}"
    else:
        source = source.split("/")[-1].split(".")[0]
    return f"counts_{source}_{datetime.now().strftime("%d-%m-%y")}.csv"

if __name__ == "__main__":
    print(getName("0"))
    print(getName("https://www.google.com")) 
    print(getName("http://localhost:8080")) 
    print(getName("sample/sample.mp4"))
    print(getName(r"C:\Users\muhammad.eehab\Documents\Code\soliton-rt-vehicle-counter"))