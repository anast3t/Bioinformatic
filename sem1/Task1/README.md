# Результаты

## SCHIZOPHRENIA 15; SCZD15 - Ген SHANK3

Ген семейства Shank. Shank - белки, которые соединяют рецепторы нейротрансмиттеров, ионные каналы и другие мембранные белки. Мутации в этом гене могут вызывать расстройства **аутистического** спектра а так же **шизофрению** 15-го типа.

Результаты `Stretcher`:
https://github.com/anast3t/Bioinformatic/blob/6611a2e7a12ab3a8bb8bab4f544685155f015581/Task%201/stretcherSHANK.stretcher#L28-L32

Результаты `Matcher`:
https://github.com/anast3t/Bioinformatic/blob/6611a2e7a12ab3a8bb8bab4f544685155f015581/Task%201/matcherSHANK.matcher#L29-L33


## SCHIZOPHRENIA 9; SCZD9 - Ген DISC1
Белок участвует в росте нейритов и развитии коры посредством взаимодействия с другими белками. 
Этот ген нарушен в транслокации t(1;11)(q42.1;q14.3), которая сегрегирует с **шизофренией типа 9** и родственными психическими расстройствами (в шотландской семье??)

Результаты `Stretcher`:
(Кусок кода не загрузился, файл сильно большой, не может показывать превью)
* Length: 415790
* Identity:   148361/415790 (35.7%)
* Similarity: 148361/415790 (35.7%)
* Gaps:       199142/415790 (47.9%)
* Score: -578855
https://github.com/anast3t/Bioinformatic/blob/6611a2e7a12ab3a8bb8bab4f544685155f015581/Task%201/stretcherDISC.stretcher#L28-L32

Результаты `Matcher`:

https://github.com/anast3t/Bioinformatic/blob/6611a2e7a12ab3a8bb8bab4f544685155f015581/Task%201/matcherDISC.matcher#L29-L33

---

## Выводы
Как можно заметить по `Score`, `Matcher` в обоих случаях отрабатывает лучше чем `Stretcher`. На DISC1 разница по всем параметрам существенно больше. Смог разрезолвить с гепами в ~4х раза меньше чем у `Stretcher`.
