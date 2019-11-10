<h1 align="center">Welcome to i18n-Crawler 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-v1.1.1-blue.svg?cacheSeconds=2592000" />
</p>

> Find instances of an i18n call tag in a source path recursively and perform a tree shake on the old translations file
>   1. Traverse ROOT_PATH recursively to find all occurrences of the i18n.t() call
>   2. Extract 'settings.account.dummy' from i18.t('settings.account.dummy')
>   3. Convert 'settings.account.dummy' to {settings: {account: {dummy: dummy }}}
>   4. Convert single dicts into a global sanitized dict with deep_merge_dicts
>   5. Intersect sanitized global dict with dirty dict from translations.js replacing leaves along the way
>   6. Convert newly merged sanitized global dict into json
>   7. Save final output to file under sanitized-dicts for later extraction
>   8. Output will be a valid Javascript object that can be injected into the translation tool
## Usage

```sh
1. replace ROOT_PATH with your root directory
2. replace DIRTY_JSON_PATH with the your old dirty json file

python3 index.py
```

