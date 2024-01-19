# Pythonic Bhashini Translator

This is a Python interface to Bhashini API, a powerful language service for Indian languages.

## Setup and use

Install `bhashini_translator` package.

```
pip install bhashini_translator
```

Befrore you can use it, you need to get necessary authentication details:

1. Sign up, register and verify your email [here](https://bhashini.gov.in/ulca/user/register).
2. Go to the profile section and generate API key.
3. Copy `userId`, `ulcaApiKey` and `InferenceApiKey`. All these values must be set in `environment` (using `dotenv` or any other way) for this to work.



```
from bhashini_translator import Bhashini

```

Translate text:

```
bhashini = Bhashini(sourceLanguage, targetLanguage)
bhashini.translate(text)
```

Text to speech, returns a base64 encoded string:

```
bhashini = Bhashini(sourceLanguage)
base64String = bhashini.tts(text)
```

Automatic speech recognition and translation to text, in target language:

```
bhashini = Bhashini(sourceLanguage, targetLanguage)
text = bhashini.asr_nmt(base64String)
```

Bashini expects us to use [ISO-639 series](https://www.loc.gov/standards/iso639-2/php/code_list.php) language codes.

Here is the list of languages supported by the IndicTrans2 models:

<table>
<tbody>
  <tr>
    <td>Assamese (asm_Beng)</td>
    <td>Kashmiri (Arabic) (kas_Arab)</td>
    <td>Punjabi (pan_Guru)</td>
  </tr>
  <tr>
    <td>Bengali (ben_Beng)</td>
    <td>Kashmiri (Devanagari) (kas_Deva)</td>
    <td>Sanskrit (san_Deva)</td>
  </tr>
  <tr>
    <td>Bodo (brx_Deva)</td>
    <td>Maithili (mai_Deva)</td>
    <td>Santali (sat_Olck)</td>
  </tr>
  <tr>
    <td>Dogri (doi_Deva)</td>
    <td>Malayalam (mal_Mlym)</td>
    <td>Sindhi (Arabic) (snd_Arab)</td>
  </tr>
  <tr>
    <td>English (eng_Latn)</td>
    <td>Marathi (mar_Deva)</td>
    <td>Sindhi (Devanagari) (snd_Deva)</td>
  </tr>
  <tr>
    <td>Konkani (gom_Deva)</td>
    <td>Manipuri (Bengali) (mni_Beng)</td>
    <td>Tamil (tam_Taml)</td>
  </tr>
  <tr>
    <td>Gujarati (guj_Gujr)</td>
    <td>Manipuri (Meitei) (mni_Mtei)</td>
    <td>Telugu (tel_Telu)</td>
  </tr>
  <tr>
    <td>Hindi (hin_Deva)</td>
    <td>Nepali (npi_Deva)</td>
    <td>Urdu (urd_Arab)</td>
  </tr>
  <tr>
    <td>Kannada (kan_Knda)</td>
    <td>Odia (ory_Orya)</td>
    <td></td>
  </tr>
</tbody>
</table>
