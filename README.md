Run with: 
`<flink_path>/bin/flink run -py <repo_path>/flink_processing.py -pyclientexec /usr/bin/python3 -pyexec /usr/bin/python3`

------

1. KAFKA PRODUCENT 1 + GENERATOR DANYCH TRANSAKCJI

    - generowanie danych takich żeby matchowały albo nie do modelu .pkl
        - model jest wytrenowany na danych 20-500$ i lokalizacji 52x20
        - więc anomalie będą występować np. dla 1$
    
    - nadanie danych z generatora na TOPIC-A


2. KAFKA CONSUMER 1 + FLINK PROCESSING + KAFKA PRODUCER 2

    - odbiera dane z TOPIC-A

    - def flink - przetwarzanie:
        - wykorzystuje wytrenowany model .pkl
        - labeluje dane 0,1 wgl modelu
    
    - nadaje dane na topic kafki = TOPIC-B


3. KAFKA CONSUMER 2

    - odbiera dane z TOPIC-B
    - wizualizacja i statystyki