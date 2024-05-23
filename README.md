

1. KAFKA PRODUCENT 1 + GENERATOR DANUCH TRANSAKCJI

    [HUBERT]

    - generuje dane
    - nadaje dane na topic kafki = TOPIC-A


2. KAFKA CONSUMER 1 + FLINK PROCESSING + KAFKA PRODUCER 2

    [MATI] + razem sie zastanowimy jak je procesowac

    - odbiera dane z TOPIC-A
    - def flink - przetwarza dane
    - nadaje przetworzone dane na topic kafki = TOPIC-B


3. KAFKA CONSUMER 2

    [RAZEM]

    - odbiera dane z TOPIC-B
    - wizualizacja i statystyki