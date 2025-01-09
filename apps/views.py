import json
from django.http import JsonResponse
from django.shortcuts import render


LOTIN_TO_KIRIL = {
    "a": "а", "b": "б", "d": "д", "e": "е", "f": "ф", "g": "г",
    "h": "ҳ", "i": "и", "j": "ж", "k": "к", "l": "л", "m": "м",
    "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с",
    "t": "т", "u": "у", "v": "в", "x": "х", "y": "й", "z": "з",
    "sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я",
    "o'": "ў", "g'": "ғ", "ng": "нг",
}

KIRIL_TO_LOTIN = {v: k for k, v in LOTIN_TO_KIRIL.items()}

def translate_text(text, to_kiril=True):
    result = []
    rules = LOTIN_TO_KIRIL if to_kiril else KIRIL_TO_LOTIN

    i = 0
    while i < len(text):

        if i + 1 < len(text) and text[i:i+2].lower() in rules:

            translated = rules[text[i:i+2].lower()]
            if text[i:i+2].isupper():
                translated = translated.upper()
            result.append(translated)
            i += 2

        elif text[i].lower() in rules:
            translated = rules[text[i].lower()]
            if text[i].isupper():
                translated = translated.upper()
            result.append(translated)
            i += 1
        else:
            result.append(text[i])
            i += 1

    return ''.join(result)

def translator_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        direction = data.get("direction", "to_kiril")
        to_kiril = direction == "to_kiril"

        translated_text = translate_text(text, to_kiril=to_kiril)
        return JsonResponse({"translated_text": translated_text})

    return render(request, "translator.html")
