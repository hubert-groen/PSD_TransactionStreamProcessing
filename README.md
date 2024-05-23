
[HUBERT]
1. KAFKA PRODUCENT 1 + GENERATOR DANUCH TRANSAKCJI

    - generuje dane
    - nadaje dane na topic kafki = TOPIC-A

[MATI] + razem sie zastanowimy jak je procesowac
2. KAFKA CONSUMER 1 + FLINK PROCESSING + KAFKA PRODUCER 2

    - odbiera dane z TOPIC-A
    - def flink - przetwarza dane
    - nadaje przetworzone dane na topic kafki = TOPIC-B

[RAZEM]
3. KAFKA CONSUMER 2

    - odbiera dane z TOPIC-B
    - wizualizacja i statystyki