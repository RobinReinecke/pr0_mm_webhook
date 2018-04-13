# pr0-Mattermost-Webhook in Python

Posting in a given interval the newest Posts from http://pr0gramm.com to a mattermost incoming webhook (https://docs.mattermost.com/developer/webhooks-incoming.html)

## example

```python
import pr0_mm_webhook

pr0_mm = pr0_mm_webhook.pr0_mm("Webhook Link here", 1, True, False, False, True)

pr0_mm.start()
```
