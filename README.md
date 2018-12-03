<h1> ECSS-10 WebTester </h1>

Python 3.5. or greater<br>
Modules are required: selenium, pyvirtualdisplay, jsonschema.<br>
Back-end: Xvfb.

<h2> [ru] </h2>

Сервис для frontend тестирования по json сценариям. 
<h3>Структура файлов</h3>

<pre>
/include
    ├──── /browser_driver_class.py
    ├──── /mult_proc_driver_class.py
    ├──── /parser_schema_class.py
    └──── /
/jsonschema
    ├──── /scenario_application_control.json
    ├──── /...
    └──── /scenario_authorization.json
/main.py
</pre>

<h4> include </h4> 
<h5> browser_driver_class </h5> 
Содержит класс ECSSWebdribe и методы взаимодействия с рабочим пространством. 
<h5> mult_proc_driver_class </h5> 
Содержит класс MultProcess, который запускает и контролирует n-e количество указанных процессов. 
<h5> parser_schema_class </h5> 
Содержит класс ParserSchemaObject, который проверяет список json словарей на соответствие схемам из указанной директории.
<h4> jsonschema </h4>
Содержит json схемы для проверки валидности web-тестов. 
<h4> main </h4>
Проверяет указанный тест на валидность и запускает driver согласно конфигурациям. 
