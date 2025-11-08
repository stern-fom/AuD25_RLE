def encode(value: str, escape='Q') -> str:
    # Initialisiert eine leere Liste, in der die kodierten Zeichenfolgen gesammelt werden
    output_list = []
    # Merkt sich das erste Zeichen der Eingabezeichenkette
    current_char = value[0]
    # Zählt, wie oft das aktuelle Zeichen direkt hintereinander vorkommt (Startwert: 1)
    current_count = 1

    # Geht jedes Zeichen der Eingabe (ab dem zweiten Zeichen) durch
    for char in value[1:]:
        # Escape-Zeichen-Behandlung:
        # Wenn das Escape-Zeichen gefunden wurde, füge die definierte Ausnahmesequenz hinzu
        if current_char == escape:
            output_list.append(escape + "@")
            current_char = char
            continue

        # Wenn das aktuelle Zeichen gleich dem gemerkten Zeichen ist,
        # wird der Zähler erhöht und die Schleife springt zum nächsten Zeichen
        if char == current_char and current_count < 26:
            current_count += 1
            continue

        # Das Zeichen hat sich geändert: kodiere die vorherige Zeichensequenz
        encode_sequence(current_char, current_count, escape, output_list)
        # Das neue Zeichen und der Zähler werden für die nächste Sequenz gesetzt
        current_char = char
        current_count = 1

    # Nach der Schleife muss die letzte Zeichensequenz noch zur Liste hinzugefügt werden
    encode_sequence(current_char, current_count, escape, output_list)

    # Die Liste wird zu einem String zusammengefügt und zurückgegeben
    return "".join(output_list)


def encode_sequence(current_char: str, current_count: int, escape: str, output_list: list[str]):
    # Wenn ein neues Zeichen beginnt,
    # prüfe, ob das vorherige Zeichen mindestens viermal hintereinander vorkam
    if 4 <= current_count <= 26:
        # Wenn ja, füge die Anzahl gefolgt vom Zeichen zur Ausgabeliste hinzu
        # Beispiel: "3A" für drei aufeinanderfolgende 'A'
        output_list.append(escape + chr(ord("A") + current_count - 1) + current_char)
    else:
        # Wenn das Zeichen nur einmal vorkam,
        # füge es einfach unverändert (ohne Anzahl) zur Ausgabeliste hinzu
        # Beispiel: "B" für ein einzelnes 'B'
        output_list.append(current_char * current_count)


def decode(value: str) -> str:
    pass

if __name__ == '__main__':
    inp = 'AAAABBBAABBBBBCCCCCCCCABCQAAA'
    out = encode(inp)
    print(inp)
    print(out)

    print("QDABBBAAQEBQHCABCQ@AAA" == out)

    inp = 'A'*30
    out = encode(inp)
    print(inp)
    print(out)
    print("QZAQDA" == out)