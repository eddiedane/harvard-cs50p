def main():
    text = input()
    emoticons = [":)", ":("]

    for emo in emoticons:
        text = text.replace(emo, convert(emo))

    print(text)

def convert(emoticon):
    match emoticon:
        case ":)":
            return "🙂"
        case ":(":
            return "🙁"
        case _:
            return emoticon

if __name__ == "__main__":
    main()