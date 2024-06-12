# PSD_TransactionStreamProcessing

## Wykrywanie Anomalii wśród Transakcji Kartami Kredytowymi przy użyciu Apache Kafka oraz Flink

**Zespół:**  
- Mateusz Zembroń
- Hubert Groen

**Repozytorium:**  
PSD_TransactionStreamProcessing

## Opis Projektu

Projekt ma na celu wykrywanie anomalii w transakcjach kartami kredytowymi poprzez przetwarzanie strumieniowe danych za pomocą Apache Kafka i Flink. System składa się z generatora danych, komponentu przetwarzania strumieniowego oraz konsumenta, który wizualizuje wyniki.

## Składniki Systemu

### Generator Danych

Symuluje transakcje kartami kredytowymi. Każdy rekord zawiera:
- `user_id`
- `card_id`
- `amount`
- `latitude`
- `longitude`
- `trans_limit`

Transakcje są generowane dla 10 użytkowników w różnych obszarach geograficznych. System jest skalowalny i może obsłużyć większą liczbę użytkowników i transakcji.

### Architektura Systemu

#### producer.py

Skrypt uruchamia generator danych, który działa jako producent Kafki. Generowane rekordy transakcji są wysyłane do topiku `TOPIC-T1`.

#### flink_processing.py

Kod Flink odbiera dane z topiku `TOPIC-T1` za pomocą integracji Kafka-Flink modułem “Source”. Strumień danych jest analizowany pod kątem wystąpienia oszustwa, a przetworzone dane są wysyłane na topik `TOPIC-T2` za pomocą modułu “Sink”.

#### st_app.py (consumer.py)

Skrypt zawiera konsumenta Kafki, który subskrybuje topik `TOPIC-T2`. W zależności od wersji skryptu, dane są wypisywane lub wizualizowane przy użyciu biblioteki Streamlit.

## Szczegóły Komponentów

### Producent

Skrypt `producer.py` generuje rekordy transakcyjne. Pierwsze n-rekordów jest generowanych bez zaburzeń, co poprawia skuteczność wykrywania anomalii metodami statystycznymi.

### Flink

Skrypt `flink_processing.py` przetwarza strumienie danych przy użyciu framework’a Flink. Dane są grupowane po numerze użytkownika za pomocą metody `key_by`. W metodzie `flat_map` dane są analizowane pod kątem anomalii, takich jak:
- Nagłe zmiany lokalizacji transakcji
- Zwiększenie częstotliwości transakcji
- Przekroczenie limitu karty
- Wyraźne zwiększenie kwoty transakcji

Informacje o średniej wartości ostatnich transakcji oraz najważniejszych parametrach transakcji są zapisywane w stanie. Do wyjściowego strumienia dołączane są informacje o wykrytych anomaliach.

### Konsument

Skrypt `st_app.py` subskrybuje topik `TOPIC-T2` i odbiera rekordy zawierające klasę detekcji (brak anomalii lub jej kategorię). Wizualizacja jest realizowana przy pomocy biblioteki Streamlit, która umożliwia stworzenie mapy z punktami lokalizacyjnymi oraz funkcjonalnych wykresów. Alternatywnie, skrypt `consumer.py` odbiera wiadomości z topiku i wypisuje je w terminalu.
