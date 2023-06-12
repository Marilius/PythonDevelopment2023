.. Chess game documentation master file, created by
   sphinx-quickstart on Sun Apr  9 18:20:50 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Chess game's documentation!
======================================
Задача - добавить на сервере MUD поддержку бродячих монстров следующим образом:

* один раз в 30 секунд выбирается случайный монстр, и он перемещается на одну клетку в случайно выбранном направлении (вправо/влево/вверх/вниз)
* если в результате перемещения монстр попал бы на клетку, где уже есть монстр, то перемещение НЕ ПРОИСХОДИТ, и проводится повторный выбор монстра и направления; и так пока не будет выполнено успешное перемещение монстра
* при перемещении сервер выдаёт всем игрокам сообщение "<имя_монстра> moved one cell <направление>", где <направление> это right, left, up, down. Например: "manticore moved one cell right"
* если монстр попадает на клетку, где есть игрок (или игроки), происходит "энкаунтер" - как если бы игрок(и) сам зашел(ли) на клетку с монстром в т.ч. монстр отрисовывается у столкнувшихся с ним игроков, с произнесением приветственной фразы

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   issue_documentation

.. include:: issue_documentation


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
