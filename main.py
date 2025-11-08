def encode(value: str) -> str:
    # Initialisiert eine leere Liste, in der die kodierten Zeichenfolgen gesammelt werden
    output_list = []
    # Merkt sich das erste Zeichen der Eingabezeichenkette
    current_char = value[0]
    # Zählt, wie oft das aktuelle Zeichen direkt hintereinander vorkommt (Startwert: 1)
    current_count = 1

    # Geht jedes Zeichen der Eingabe (ab dem zweiten Zeichen) durch
    for char in value[1:]:
        # Wenn das aktuelle Zeichen gleich dem gemerkten Zeichen ist,
        # wird der Zähler erhöht und die Schleife springt zum nächsten Zeichen
        if char == current_char:
            current_count += 1
            continue

        # Wenn ein neues Zeichen beginnt,
        # prüfe, ob das vorherige Zeichen mindestens zweimal hintereinander vorkam
        if current_count >= 2:
            # Wenn ja, füge die Anzahl gefolgt vom Zeichen zur Ausgabeliste hinzu
            # Beispiel: "3A" für drei aufeinanderfolgende 'A'
            output_list.append(str(current_count) + current_char)
        else:
            # Wenn das Zeichen nur einmal vorkam,
            # füge es einfach unverändert (ohne Anzahl) zur Ausgabeliste hinzu
            # Beispiel: "B" für ein einzelnes 'B'
            output_list.append(current_char * current_count)
        # Das neue Zeichen und der Zähler werden für die nächste Sequenz gesetzt
        current_char = char
        current_count = 1

    # Nach der Schleife muss die letzte Zeichensequenz noch zur Liste hinzugefügt werden
    output_list.append(str(current_count) + current_char)

    # Die Liste wird zu einem String zusammengefügt und zurückgegeben
    return "".join(output_list)

def decode(value: str) -> str:
    pass

if __name__ == '__main__':
    out = encode('AAAABBBAABBBBBCCCCCCCCABCQAAA')

    print("4A3B2A5B8CABCQ3A" == out)