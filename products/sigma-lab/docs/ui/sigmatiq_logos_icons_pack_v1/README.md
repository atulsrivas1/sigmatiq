# Sigmatiq Logos & Icons Pack (v1)

Primary brand: **Sigmatiq** (domain: https://sigmatiq.ai)  
Sub-brand: **Sigmatiq Sigma**  
Packs: **ZeroSigma**, **SwingSigma**, **LongSigma**, **OvernightSigma**, **CustomizedSigma**.

## Structure
```
sigmatiq/
  svg/sigmatiq_mark.svg
  svg/sigmatiq_lockup_horizontal.svg
  png/sigmatiq_mark_{2048,1024,512,256,128,64,32}.png
  favicon.ico
sigmatiq_sigma/
  svg/sigmatiq_edge_mark.svg
  svg/sigmatiq_edge_lockup_horizontal.svg
  png/sigmatiq_edge_mark_{sizes}.png
  favicon.ico
packs/{zerosigma|swingsigma|longsigma|overnightsigma|customizededge}/
  svg/*_mark.svg, *_lockup_horizontal.svg
  png/*_mark_{sizes}.png
  favicon.ico
ui_icons/svg/*.svg
sigmatiq-brand.css
colors.json
```

## Usage
```html
<img src="/sigmatiq/svg/sigmatiq_mark.svg" alt="Sigmatiq" width="128">
<img src="/sigmatiq_sigma/png/sigmatiq_edge_mark_512.png" alt="Sigmatiq Sigma" width="128">
<link rel="stylesheet" href="/sigmatiq-brand.css">
```

**Accent theming per pack**
```html
<html data-sigma="swing">
  <button class="accent-bg">Run</button>
</html>
```

## Colors
- Sigmatiq: #0A2540
- Sigmatiq Sigma accent: #1ABC9C
- ZeroSigma: #3B82F6 · SwingSigma: #F97316 · LongSigma: #22C55E · OvernightSigma: #8B5CF6 · CustomizedSigma: #14B8A6

> SVG for crisp scaling; PNGs for legacy/favicons. Back-compat CSS aliases provided for older `--sig-*` tokens.
