#!/bin/bash

APP_URL="https://projetmassivedata.appspot.com/api/timeline?user=user1&limit=20"
OUT="../../out/conc.csv"

NREQ=200
TIMEOUT=30

echo "PARAM,AVG_TIME,RUN,FAILED" > $OUT

run_bench() {
    C=$1
    RUN=$2

    OUTPUT=$(hey -t ${TIMEOUT} -n $NREQ -c $C $APP_URL 2>&1)

    # Extraire "Average" en sec
    AVG_SEC=$(echo "$OUTPUT" | grep "Average" | awk '{print $2}')

    # Si vide → on met une valeur spéciale (ex: -1)
    if [ -z "$AVG_SEC" ]; then
        AVG_MS=-1
    else
        AVG_MS=$(awk "BEGIN {print $AVG_SEC * 1000}")
    fi

    FAILED=$(echo "$OUTPUT" | grep "Non-2xx" | awk '{print $2}')
    if [ -z "$FAILED" ]; then
        FAILED=0
    fi

    echo "$C,$AVG_MS,$RUN,$FAILED"
}

for C in 1 10 20 50 100 1000; do
    for RUN in 1 2 3; do
        run_bench $C $RUN >> $OUT
    done
done

echo "Expérience 1 : Benchmarks terminés."
