# Notify

[`notify.py`](notify.py) defines an interface for notifications service, based on Builder creational pattern.



## Interface documentation

Each service provides methods for text insertion. They all return `self`.

> They <u>all insert a line break in the end</u>. To remove the line break, some (marked in the table below) support the parameter `end`. Example below.
>
> ```python
> .heading("This is a heading", end="")
> ```

| Method      | Argument                    | Description                                                  | end param |
| ----------- | --------------------------- | ------------------------------------------------------------ | --------- |
| heading     | h1:str                      | Text heading                                                 | Yes       |
| heading2    | h2:str                      | Text heading                                                 | Yes       |
| text        | text:str                    | Simple text                                                  | Yes       |
| information | title:str<br />info:str     | Information card                                             | Yes       |
| button      | title:str<br />text:str     | Button with link                                             | Yes       |
| card        | title:str<br />content:list | Card with content, tha is list of objects {"name": str, "value": str} | Yes       |
| code        | block:str                   | Code block                                                   | No        |
| clean       |                             | Returns empty notification builder.                          | No        |

For text decoration, the following methods are available. They all return `str`.

| Method | Argument | Description | end param |
| ------ | -------- | ----------- | --------- |
| bold   | text:str | Bold text   | Yes       |
| italic | text:str | Italic text | Yes       |

Finally to send the message through the service, use `send(subject:str, preview:str, recipient:str) -> int`, which returns the HTTP status code of the sent message process.



## Microsoft Teams

Teams integration is at file [`teams.py`](teams.py).

>  The Slack integration was created based on an official tutorial that can be found [here](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook).



## Email

Email integration is at file [email.py](email.py).

