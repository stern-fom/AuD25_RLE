def encode(value: bytes, escape=b'Q') -> bytes:
    # Initialisiert eine leere Liste, in der die kodierten Zeichenfolgen gesammelt werden
    output_list = []
    # Merkt sich das erste Zeichen der Eingabezeichenkette
    current_char = value[:1]
    # Zählt, wie oft das aktuelle Zeichen direkt hintereinander vorkommt (Startwert: 1)
    current_count = 1

    # Geht jedes Zeichen der Eingabe (ab dem zweiten Zeichen) durch
    for char in value[1:]:
        # Escape-Zeichen-Behandlung:
        # Wenn das Escape-Zeichen gefunden wurde, füge die definierte Ausnahmesequenz hinzu
        if current_char[0] == escape[0]:
            output_list.append(escape + b"@")
            current_char = bytes([char])
            continue

        # Wenn das aktuelle Zeichen gleich dem gemerkten Zeichen ist,
        # wird der Zähler erhöht und die Schleife springt zum nächsten Zeichen
        if char == current_char[0] and current_count < 26:
            current_count += 1
            continue

        # Das Zeichen hat sich geändert: kodiere die vorherige Zeichensequenz
        encode_sequence(current_char, current_count, escape, output_list)
        # Das neue Zeichen und der Zähler werden für die nächste Sequenz gesetzt
        current_char = bytes([char])
        current_count = 1

    # Nach der Schleife muss die letzte Zeichensequenz noch zur Liste hinzugefügt werden
    encode_sequence(current_char, current_count, escape, output_list)

    # Die Liste wird zu einem String zusammengefügt und zurückgegeben
    return b"".join(output_list)


def encode_sequence(current_char: bytes, current_count: int, escape: bytes, output_list: list[bytes]):
    # Wenn ein neues Zeichen beginnt,
    # prüfe, ob das vorherige Zeichen mindestens viermal hintereinander vorkam
    if 4 <= current_count <= 26:
        # Wenn ja, füge die Anzahl gefolgt vom Zeichen zur Ausgabeliste hinzu
        # Beispiel: "3A" für drei aufeinanderfolgende 'A'
        output_list.append(escape + chr(ord("A") + current_count - 1).encode() + current_char)
    else:
        # Wenn das Zeichen nur einmal vorkam,
        # füge es einfach unverändert (ohne Anzahl) zur Ausgabeliste hinzu
        # Beispiel: "B" für ein einzelnes 'B'
        output_list.append(current_char * current_count)


def decode(value: bytes, escape=b"Q") -> bytes:
    # Zustandsvariable: 0 = IDLE (normaler Modus), 1 = ESCAPE (Escape-Zeichen erkannt), 2 = COUNT (Anzahl erkannt)
    state = 0
    # Variable zur Speicherung der Anzahl bei RLE-Sequenzen
    count = 0
    # Liste zur Sammlung der Ausgabezeichen
    output_list = []
    # Jedes Byte der Eingabe wird einzeln verarbeitet
    for char in value:
        if state == 0:  # IDLE: Normaler Modus
            # Wenn das aktuelle Zeichen kein Escape-Zeichen ist, wird es direkt zur Ausgabe hinzugefügt
            if char != escape[0]:
                output_list.append(bytes([char]))
            else:
                # Wenn das Escape-Zeichen erkannt wird, wechsel in den ESCAPE-Zustand
                state = 1
        elif state == 1:  # ESCAPE: Escape-Zeichen wurde erkannt
            # Wenn das nächste Zeichen ein "@" ist, handelt es sich um den Sonderfall: Escape-Zeichen ausgeben
            if bytes([char]) == b"@":
                output_list.append(escape)
                state = 0  # Zurück zum IDLE-Zustand
            else:
                # Ansonsten wird das nächste Zeichen als Anzahl interpretiert (A=1, B=2, ...)
                count = char - ord("A") + 1
                state = 2  # Wechsel in den COUNT-Zustand
        elif state == 2:  # COUNT: Anzahl wurde erkannt
            # Das aktuelle Zeichen wird entsprechend der Anzahl zur Ausgabe hinzugefügt
            output_list.append(bytes([char]) * count)
            count = 0  # Anzahl zurücksetzen
            state = 0  # Zurück zum IDLE-Zustand
        else:
            # Fehlerfall: Unbekannter Zustand
            print("ERROR")
    # Prüfung auf unvollständige Sequenz am Ende der Eingabe
    if state != 0:
        print("ERROR: Unvollständige Sequenz")
    # Zusammenfügen der Ausgabe-Liste zu einem Bytes-Objekt und Rückgabe
    return b"".join(output_list)

if __name__ == '__main__':
    inp = b'AAAABBBAABBBBBCCCCCCCCABCQAAA'
    out = encode(inp)
    print(inp)
    print(out)

    print(b"QDABBBAAQEBQHCABCQ@AAA" == out)

    inp = b'A'*30
    out = encode(inp)
    print(inp)
    print(out)
    print(b"QZAQDA" == out)

    inp = b"QDABBBAAQEBQHCABCQ@AAA"
    out = decode(inp)
    print(inp)
    print(out)
    print(b'AAAABBBAABBBBBCCCCCCCCABCQAAA' == out)

    inp = b"QZAQDA"
    out = decode(inp)
    print(inp)
    print(out)
    print(b'A'*30 == out)

    with open("hallo_256.bmp", "rb") as f:
        img = f.read()

    out = encode(img)
    with open("hallo_256.arl", "wb") as f:
        f.write(out)

    with open("hallo_256.arl", "rb") as f:
        rle_img = f.read()
    out = decode(rle_img)
    with open("hallo_256_restored.bmp", "wb") as f:
        f.write(out)