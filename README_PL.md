# Wtyczka EX-Torrenty


**Wersja Wtyczki:** 3.3.1
**Wersja Dokumentacji 1.01
**Autor:** KordianJ (5c0rp10n) kordian2025@gmail.com
**Współautor:** powerzasty
**Podziękowania:** ex-torrenty.com
**Licencja:** GPLv3+
**Data Ostatniej Modyfikacji:** 15.10.2025

---

## Przegląd

`ex_torrenty.py` to wtyczka w Pythonie, która pozwala wyszukiwać i pobierać torrenty z [EX-Torrenty](https://ex-torrenty.org/) poprzez ich API.
Wtyczka pobiera metadane torrentów i obsługuje pobieranie plików `.torrent` z użyciem ciasteczek sesyjnych do autoryzacji.

Wtyczka wykorzystuje z **`novaprinter`**, zgodnie z dokumentacją qBittorent** 

---

## Dołączone pliki

Wtyczka korzysta z następujących modułów pomocniczych, dostarczonych pierwotnie przez **qBittorent**:

* `helpers.py` 
* `nova2.py` 
* `nova2dl.py` 
* `novaprinter.py` 
* `socks.py` 

> ⚠️ Zaleca się sprawdzenie, czy nie istnieją nowsze wersje tych plików przed użyciem.

Dodatkowo załączony jest katalog install gdzie znajduję skrypt python generujący ciasteczka. 
---

## Dokumentacja Oficjalna

Oficjalna dokumentacja tworzenia wtyczek, jest dostępna na GitHubie:

[Dokumentacja plugin-ów qBittorent](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin)

---

## Wymagania

Nie ma konieczności instalowania dodatkowych pakietów, jeśli wtyczka ma być używana w podstawowej formie. Wystarczy zainstalować zgodnie z dokuemtnacją QtBiTorent. Plik requiments dodany dla wygody. 

---

## Konfiguracja – Ciasteczka

⚠️ **Ważne:** Aby wtyczka działała, musisz podać **ciasteczka sesyjne z własnego konta EX-Torrenty**.

1. Zaloguj się na [EX-Torrenty](https://ex-torrenty.org/) w przeglądarce.
2. Pobierz następujące ciasteczka z sesji:

   * `uid`
   * `pass`
   * `hashv`
   * `PHPSESSID`
3. Zamień wartości w słowniku `COOKIES` w pliku `ex_torrenty.py` na swoje ciasteczka. Przykład:

```python
COOKIES = {
    "uid": "xxxxxx",
    "pass": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "hashv": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "PHPSESSID": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

> Wtyczka nie będzie działać bez poprawnych ciasteczek sesyjnych.

---

### Automatyczny generator ciasteczek

W katalogu `install/` znajduje się skrypt pomocniczy, który generuje plik JSON z odpowiednimi ciasteczkami dla Twojej sesji:

* `instalator.py` 

potrzebne do uruchomienia pakiety to:

* `beautifulsoup4>=4.12.0`
* `selenium>=4.21.0`

---

## Użytkowanie poza qBittorent**

Wtyczke można przetestować w terminalu. 
Pierwszy wynik wyszukiwania jest pobierany automatycznie 

---

## Licencja

Wtyczka jest wydana na **licencji GPLv3+**.
Możesz ją używać, modyfikować i rozpowszechniać.
Korzystasz na własne ryzyko.

> ⚠️ Użytkownicy są odpowiedzialni za legalność pobierania treści w swoim kraju.
