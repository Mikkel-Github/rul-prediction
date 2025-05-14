/*
    Custom CSV parser to handle the response from the backend.
*/
codeunit 50100 "Simple CSV Parser"
{
    procedure LoadFromStream(var InS: InStream; Separator: Text): List of [Text[1000]]
    var
        Line: Text;
        Rows: List of [Text[1000]];
    begin
        while not InS.EOS do begin
            InS.ReadText(Line);
            Rows.Add(Line);
        end;
        exit(Rows);
    end;

    procedure ParseLine(Line: Text; Separator: Text): array[10] of Text
    var
        Result: array[10] of Text;
        i: Integer;
        currentField: Text;
        fieldIndex: Integer;
        char: Text[1];
        inQuotes: Boolean;
    begin
        fieldIndex := 1;
        for i := 1 to StrLen(Line) do begin
            char := CopyStr(Line, i, 1);
            case char of
                '"':
                    inQuotes := not inQuotes;
                Separator:
                    if not inQuotes then begin
                        Result[fieldIndex] := currentField;
                        currentField := '';
                        fieldIndex += 1;
                    end else
                        currentField += char;
                else
                    currentField += char;
            end;
        end;

        Result[fieldIndex] := currentField;
        exit(Result);
    end;
}
