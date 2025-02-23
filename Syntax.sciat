;DEFINE :task(load_data) → ;MAP[loc = "/data/input.csv"]
;EXECUTE :task(load_data) → ;CALLFUNC(parse_csv, :loc)

;LOOP (i : 0 → 10) {
    ;RUN process_chunk(:i) → ;CHECK result
}

;FINALIZE → ;SAVE result → "/data/output.bin"
