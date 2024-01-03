# Findings

## Logging in

### What happens:

- A request ( POST ) is sent to the following URL: " https://meridianbet.rs/rest/mob/exec "

- Payload: 

```json
{"type":"CheckLoginAction","action":{}}
```
- Headers

```
Accept:
application/json
Accept-Encoding:
gzip, deflate, br
Accept-Language:
en-US,en;q=0.9
Authorization:
df2ccdf95ec2813c1a0c971463052ae3dd5c4e4453a6d15959853d402aa85032
Content-Length:
39
Content-Type:
application/json
Cookie:
should_redirect_last_visited_page=false; locale=sr; first_time_visit_site=0; clientsessionid=1702992781
Dnt:
1
Language:
sr
Origin:
https://meridianbet.rs
Referer:
https://meridianbet.rs/sr/kladjenje?login=true
Sec-Ch-Ua:
"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"
Sec-Ch-Ua-Mobile:
?0
Sec-Ch-Ua-Platform:
"macOS"
Sec-Fetch-Dest:
empty
Sec-Fetch-Mode:
cors
Sec-Fetch-Site:
same-origin
User-Agent: RANDOM
```

### Needed:

- Authorization header
- clientsessionid




## Tokens

## CF

