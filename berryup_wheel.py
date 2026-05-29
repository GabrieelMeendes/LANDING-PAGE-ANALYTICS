"""Roleta de desconto Berry Up — sempre prêmio máximo; CTAs até girar."""

from __future__ import annotations

import math
import re

WHEEL_ID = "berryup-roleta"
HERO_BLOCK_ID = "b_1002625_1_173566432642604808"
HERO_BOX_EID = "e_1002625_1_173566432642608997"
HERO_CARD_TEXT_EID = "e_1002625_1_173566432642692958"
HERO_CARD_FOOTER_EID = "e_1002625_1_173566432642628699"
HERO_BTN_EID = "e_1002625_1_173566432642648538"
HERO_IMG_EID = "e_1002625_1_173566432642696494"
HERO_TITLE_EID = "e_1002625_1_173566432642603045"
HERO_KICKER_EID = "e_1002625_1_173566432642615795"
HERO_HEADLINE_EID = "e_1002625_1_173566432642658588"
HERO_ARROW_EID = "e_1002625_1_173566432642622187"
DEPOIMENTOS_NEXT_CTA_PREFIX = "e_1002625_1_17307234956728bea7e6bc6088578960"
RESULT_CTA_BLOCK_ID = "b_1002625_1_17307234956728bea7c7c46"
BUY_CTA_BLOCK_ID = "b_1002625_1_17307234956728bea7c7c49"
SEVEN_DAYS_CTA_BLOCK_ID = "b_1002625_1_174828414165505023"
SEVEN_DAYS_BTN_EID = "e_1002625_1_174828414165512806"
SEVEN_DAYS_FOOTER_EID = "e_1002625_1_174828414165541607"
PRIZE_BAR_ID = "berryup-prize-bar"
WIN_MODAL_ID = "berryup-win-modal"
STORAGE_MODAL_DISMISSED = "berryup_win_modal_dismissed_v1"
BESTSELLER_BAR_BLOCK_ID = "b_1002625_1_174828396566595021"
BESTSELLER_TEXT_EID = "e_1002625_1_174828396566515887"
WHEEL_SCRIPT_ID = "berryup-wheel-script"
WHEEL_DISCOUNT = 60
WHEEL_TIMER_SEC = 300
EBOOK_LIST_PRICE = 97.0
EBOOK_INSTALLMENTS = 6
STORAGE_WON = "berryup_wheel_won_v1"
STORAGE_EXPIRES = "berryup_wheel_expires_v1"

# Amarelo sólido da referência Peach Up (sem gradiente laranja)
BERRYUP_CTA_YELLOW = "#FFF133"
BERRYUP_CTA_ORANGE = "#ff6316"

BERRYUP_CTA_YELLOW_CSS = f"""
/* Centralizar wrappers GreatPages dos CTAs checkout (amarelo/laranja) */
body.berryup-wheel-won .gpc-e.e_botao.berryup-cta-wrap-centered:not(#{HERO_BTN_EID}):not([id^="{DEPOIMENTOS_NEXT_CTA_PREFIX}"]):not(#{SEVEN_DAYS_BTN_EID}),
body.berryup-wheel-won .gpc-e.e_botao:has(a.berryup-checkout-cta.berryup-cta-ready):not(#{HERO_BTN_EID}):not([id^="{DEPOIMENTOS_NEXT_CTA_PREFIX}"]):not(#{SEVEN_DAYS_BTN_EID}){{
  left:50%!important;right:auto!important;transform:translateX(-50%)!important;
  width:min(420px,92vw)!important;max-width:92vw!important;height:auto!important;box-sizing:border-box!important}}
@media(min-width:801px){{
body.berryup-wheel-won .gpc-e.e_botao.berryup-cta-wrap-centered:not(#{HERO_BTN_EID}):not([id^="{DEPOIMENTOS_NEXT_CTA_PREFIX}"]):not(#{SEVEN_DAYS_BTN_EID}),
body.berryup-wheel-won .gpc-e.e_botao:has(a.berryup-checkout-cta.berryup-cta-ready):not(#{HERO_BTN_EID}):not([id^="{DEPOIMENTOS_NEXT_CTA_PREFIX}"]):not(#{SEVEN_DAYS_BTN_EID}){{
  width:min(420px,44vw)!important;max-width:480px!important}}}}
body.berryup-wheel-won .gpc-e.e_botao.berryup-cta-wrap-centered .c,
body.berryup-wheel-won .gpc-e.e_botao:has(a.berryup-checkout-cta.berryup-cta-ready) .c{{
  width:100%!important;height:auto!important;display:flex!important;
  justify-content:center!important;align-items:center!important;text-align:center!important}}
body.berryup-wheel-won .gpc-e.e_botao.berryup-cta-wrap-centered a.berryup-checkout-cta.berryup-cta-ready,
body.berryup-wheel-won .gpc-e.e_botao:has(a.berryup-checkout-cta.berryup-cta-ready) a.berryup-checkout-cta.berryup-cta-ready{{
  position:relative!important;left:auto!important;top:auto!important;right:auto!important;
  transform:none!important;margin:0 auto!important;width:100%!important;max-width:100%!important}}
/* Botões checkout — amarelo {BERRYUP_CTA_YELLOW}, texto preto (referência Peach Up) */
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready,
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready.c,
body.berryup-wheel-won a.e_botao.berryup-checkout-cta.berryup-cta-ready,
body.berryup-wheel-won a.e_botao.berryup-checkout-cta.berryup-cta-ready.c{{
  display:inline-flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;
  gap:5px!important;text-align:center!important;line-height:1.15!important;white-space:normal!important;text-decoration:none!important;
  padding:16px 32px!important;min-height:58px!important;height:auto!important;width:auto!important;max-width:min(100%,420px);
  background:{BERRYUP_CTA_YELLOW}!important;background-color:{BERRYUP_CTA_YELLOW}!important;background-image:none!important;
  border:none!important;border-radius:999px!important;
  box-shadow:0 4px 14px rgba(0,0,0,.14)!important;
  color:#1a1a1a!important;box-sizing:border-box!important;font-weight:800!important;
  text-shadow:none!important;filter:none!important}}
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready:hover,
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready.c:hover,
body.berryup-wheel-won a.e_botao.berryup-checkout-cta.berryup-cta-ready:hover{{
  filter:brightness(1.03)!important;box-shadow:0 6px 18px rgba(0,0,0,.18)!important;transform:translateY(-1px)!important;color:#1a1a1a!important}}
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-tag,
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-tag *{{
  display:inline-block;font-size:clamp(.85rem,2.6vw,.95rem)!important;font-weight:800!important;
  letter-spacing:.08em;text-transform:uppercase;
  background:rgba(0,0,0,.08)!important;border:none!important;border-radius:999px!important;
  padding:4px 14px!important;line-height:1.25;color:#1a1a1a!important;text-shadow:none!important}}
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main,
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main-text,
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main *{{
  display:block;font-size:clamp(1.05rem,3.4vw,1.28rem)!important;font-weight:800!important;
  color:#1a1a1a!important;letter-spacing:.02em;text-shadow:none!important}}
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-sub,
#berryup-roleta .br-cta-main.berryup-cta-ready .berryup-cta-sub{{
  display:block!important;font-size:clamp(.72rem,2.4vw,.86rem)!important;
  font-weight:800!important;line-height:1.2!important;color:#5b3c00!important;
  letter-spacing:0!important;text-transform:none!important;text-shadow:none!important}}
body.berryup-wheel-won #{SEVEN_DAYS_CTA_BLOCK_ID} a.berryup-checkout-cta.berryup-cta-ready,
body.berryup-wheel-won #{SEVEN_DAYS_CTA_BLOCK_ID} a.e_botao.berryup-checkout-cta.berryup-cta-ready{{
  background:linear-gradient(180deg,#ff7a35,{BERRYUP_CTA_ORANGE})!important;background-color:{BERRYUP_CTA_ORANGE}!important;
  color:#fff!important;box-shadow:0 4px 0 #d94e0a,0 8px 20px rgba(255,99,22,.35)!important}}
body.berryup-wheel-won #{SEVEN_DAYS_CTA_BLOCK_ID} a.berryup-checkout-cta.berryup-cta-ready:hover,
body.berryup-wheel-won #{SEVEN_DAYS_CTA_BLOCK_ID} a.e_botao.berryup-checkout-cta.berryup-cta-ready:hover{{
  color:#fff!important;filter:brightness(1.05)!important}}
body.berryup-wheel-won #{SEVEN_DAYS_CTA_BLOCK_ID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-tag,
body.berryup-wheel-won #{SEVEN_DAYS_CTA_BLOCK_ID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-tag *{{
  background:rgba(255,255,255,.22)!important;color:#fff!important}}
body.berryup-wheel-won #{SEVEN_DAYS_CTA_BLOCK_ID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main,
body.berryup-wheel-won #{SEVEN_DAYS_CTA_BLOCK_ID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main *{{
  color:#fff!important;font-size:clamp(.95rem,3.2vw,1.15rem)!important;letter-spacing:.04em;text-transform:uppercase}}
#{SEVEN_DAYS_CTA_BLOCK_ID} #{SEVEN_DAYS_BTN_EID}.gpc-e.e_botao,
#{SEVEN_DAYS_CTA_BLOCK_ID} #{SEVEN_DAYS_BTN_EID}.gpc-e.e_botao.berryup-cta-wrap-centered{{
  left:50%!important;transform:translateX(-50%)!important;
  width:min(340px,92vw)!important;max-width:92vw!important;height:auto!important}}
#{SEVEN_DAYS_CTA_BLOCK_ID} #{SEVEN_DAYS_FOOTER_EID}{{
  z-index:1520!important;text-align:center!important;width:auto!important}}
@media(max-width:800px){{
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready,
body.berryup-wheel-won a.e_botao.berryup-checkout-cta.berryup-cta-ready{{
  padding:18px 24px!important;min-height:62px!important;width:min(100%,340px)!important;max-width:92vw!important}}
body.berryup-wheel-won #{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready,
body.berryup-wheel-won #{HERO_BLOCK_ID} #{HERO_BTN_EID} a.e_botao.berryup-checkout-cta.berryup-cta-ready{{
  flex-direction:column!important;gap:4px!important;padding:12px 18px!important;
  min-height:58px!important;width:100%!important;max-width:100%!important}}
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main,
body.berryup-wheel-won a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main-text{{
  font-size:clamp(1.08rem,4.2vw,1.22rem)!important}}
body.berryup-wheel-won #{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main,
body.berryup-wheel-won #{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main *{{
  font-size:clamp(.98rem,3.8vw,1.12rem)!important}}
}}
#berryup-roleta .br-cta-main.berryup-cta-ready{{
  display:inline-flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;
  gap:5px!important;
  background:{BERRYUP_CTA_YELLOW}!important;background-image:none!important;
  border:none!important;border-radius:999px!important;
  box-shadow:0 4px 14px rgba(0,0,0,.14)!important;
  padding:16px 32px!important;min-height:58px!important;color:#1a1a1a!important;font-weight:800!important}}
#berryup-roleta .br-cta-main.berryup-cta-ready:hover{{
  filter:brightness(1.03);box-shadow:0 6px 18px rgba(0,0,0,.18)!important;color:#1a1a1a!important}}
#berryup-roleta .br-cta-main.berryup-cta-ready .berryup-cta-tag{{
  font-size:clamp(.85rem,2.6vw,.95rem)!important;font-weight:800!important;letter-spacing:.08em;text-transform:uppercase;
  background:rgba(0,0,0,.08)!important;border:none!important;border-radius:999px!important;
  padding:4px 14px!important;color:#1a1a1a!important}}
#berryup-roleta .br-cta-main.berryup-cta-ready .berryup-cta-main-text{{
  font-size:clamp(1.05rem,3.4vw,1.28rem)!important;font-weight:800!important;color:#1a1a1a!important}}
/* Hero — caixa branca: fundo atrás do texto + botão */
#{HERO_BLOCK_ID} #{HERO_BOX_EID}{{
  z-index:1505!important;pointer-events:none!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID}{{
  z-index:1512!important;height:auto!important;pointer-events:none!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID} .c,
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID} .c p,
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID} .c span{{
  line-height:1.45!important;white-space:normal!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_FOOTER_EID}{{
  z-index:1513!important;height:auto!important;pointer-events:none!important}}
#{HERO_BLOCK_ID} #{HERO_BTN_EID}.gpc-e.e_botao,
#{HERO_BLOCK_ID} #{HERO_BTN_EID}.gpc-e.e_botao.berryup-cta-wrap-centered{{
  transform:none!important;box-sizing:border-box!important;z-index:1515!important}}
#{HERO_BLOCK_ID} #{HERO_BTN_EID} .c,
#{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready{{
  width:100%!important;max-width:100%!important;display:flex!important;justify-content:center!important;
  align-items:center!important}}
/* Hero — botão amarelo estilo Peach Up (referência: pill, ~20px, caps) */
#{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready,
#{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready.c{{
  flex-direction:row!important;flex-wrap:wrap!important;gap:8px 12px!important;
  padding:14px 26px!important;min-height:52px!important;height:auto!important;
  border-radius:100px!important;box-shadow:rgb(207,207,207) 0 1px 3px!important;
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif!important;
  font-size:clamp(1.05rem,2.4vw,1.27rem)!important;font-weight:800!important;
  letter-spacing:.02em!important;text-transform:uppercase!important;color:#242424!important;
  background:#FFF133!important;background-color:#FFF133!important}}
#{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-tag,
#{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-tag *{{
  font-size:clamp(.7rem,1.8vw,.78rem)!important;padding:2px 10px!important;
  text-transform:uppercase!important;letter-spacing:.06em!important}}
#{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main,
#{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main,
#{HERO_BLOCK_ID} #{HERO_BTN_EID} a.berryup-checkout-cta.berryup-cta-ready .berryup-cta-main *{{
  font-size:clamp(1.05rem,2.4vw,1.27rem)!important;font-weight:800!important;
  text-transform:uppercase!important;letter-spacing:.02em!important;color:#242424!important}}
@media(min-width:801px){{
/* Hero desktop — espaço entre kicker amarelo e headline branca */
#{HERO_BLOCK_ID} #{HERO_TITLE_EID}{{
  top:108px!important;left:-132px!important;transform:none!important}}
#{HERO_BLOCK_ID} #{HERO_KICKER_EID}{{
  top:192px!important;left:-132px!important;width:min(720px,52vw)!important;
  max-width:min(720px,52vw)!important;height:auto!important;transform:none!important;
  line-height:1.32!important}}
#{HERO_BLOCK_ID} #{HERO_KICKER_EID} .c p,
#{HERO_BLOCK_ID} #{HERO_KICKER_EID} .c p b{{
  line-height:1.32!important;margin:0!important}}
#{HERO_BLOCK_ID} #{HERO_HEADLINE_EID}{{
  top:312px!important;left:-132px!important;width:min(720px,52vw)!important;
  max-width:min(720px,52vw)!important;height:auto!important;transform:none!important}}
#{HERO_BLOCK_ID} #{HERO_HEADLINE_EID} .c h1,
#{HERO_BLOCK_ID} #{HERO_HEADLINE_EID} .c h1 span{{
  font-size:32px!important;line-height:1.2!important;margin:0!important}}
#{HERO_BLOCK_ID} #{HERO_BOX_EID}{{
  left:-132px!important;top:483px!important;width:484px!important;height:243px!important;
  transform:none!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID}{{
  left:-93px!important;top:501px!important;width:418px!important;max-width:418px!important;
  transform:none!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID} .c{{font-size:20px!important;line-height:1.5!important;text-align:center!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_FOOTER_EID}{{
  left:50%!important;top:710px!important;width:auto!important;max-width:280px!important;
  transform:translateX(-50%)!important;text-align:center!important}}
#{HERO_BLOCK_ID} #{HERO_BTN_EID}.gpc-e.e_botao,
#{HERO_BLOCK_ID} #{HERO_BTN_EID}.gpc-e.e_botao.berryup-cta-wrap-centered{{
  left:-93px!important;top:633px!important;width:406px!important;max-width:406px!important;
  height:auto!important;min-height:54px!important}}
}}
@media(max-width:800px){{
/* Hero mobile — títulos + caixa branca (posição fina via layoutHeroCard JS) */
#{HERO_BLOCK_ID}{{
  height:auto!important;min-height:0!important;padding-bottom:20px!important;overflow:visible!important}}
#{HERO_BLOCK_ID} .centralizar{{
  min-height:0!important;height:auto!important;overflow:visible!important}}
#{HERO_BLOCK_ID} #{HERO_TITLE_EID}{{
  left:50%!important;top:clamp(2px,1.2vw,8px)!important;
  transform:translateX(-50%)!important;width:min(92vw,360px)!important;
  max-width:92vw!important;height:auto!important;z-index:1514!important}}
#{HERO_BLOCK_ID} #{HERO_KICKER_EID}{{
  left:50%!important;top:clamp(38px,9vw,54px)!important;
  transform:translateX(-50%)!important;width:min(94vw,420px)!important;
  max-width:94vw!important;height:auto!important;z-index:1513!important}}
#{HERO_BLOCK_ID} #{HERO_KICKER_EID} .c p,
#{HERO_BLOCK_ID} #{HERO_KICKER_EID} .c p b{{
  white-space:normal!important;line-height:1.25!important;margin:0!important}}
#{HERO_BLOCK_ID} #{HERO_KICKER_EID} .c p b{{
  font-size:clamp(.88rem,3.6vw,1.08rem)!important;display:block!important}}
#{HERO_BLOCK_ID} #{HERO_HEADLINE_EID}{{
  left:50%!important;top:clamp(92px,24vw,118px)!important;
  transform:translateX(-50%)!important;width:min(92vw,362px)!important;
  max-width:92vw!important;height:auto!important;z-index:1512!important;
  padding:10px 14px 12px!important;box-sizing:border-box!important;
  background:rgba(255,255,255,.1)!important;border:2px solid #fff!important;
  border-radius:12px!important;box-shadow:0 4px 18px rgba(0,0,0,.15)!important}}
#{HERO_BLOCK_ID} #{HERO_HEADLINE_EID} .c h1,
#{HERO_BLOCK_ID} #{HERO_HEADLINE_EID} .c h1 span{{
  font-size:20px!important;text-align:center!important;line-height:1.15!important}}
#{HERO_BLOCK_ID} #{HERO_BOX_EID}{{
  left:50%!important;transform:translateX(-50%)!important;
  width:min(366px,92vw)!important;height:auto!important;min-height:0!important;
  box-sizing:border-box!important;z-index:1505!important}}
#{HERO_BLOCK_ID} #{HERO_BOX_EID} .c,
#{HERO_BLOCK_ID} #{HERO_BOX_EID} .c.e_caixa,
#{HERO_BLOCK_ID} #{HERO_BOX_EID} .c.borda_igual{{
  background:#fff!important;border:2px solid #fff!important;border-radius:14px!important;
  box-shadow:0 8px 28px rgba(0,0,0,.16)!important;width:100%!important;
  min-height:100%!important;height:100%!important;box-sizing:border-box!important;
  display:block!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID}{{
  left:50%!important;transform:translateX(-50%)!important;
  width:min(320px,88vw)!important;max-width:88vw!important;
  padding:16px 14px 0!important;box-sizing:border-box!important;z-index:1512!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID} .c,
#{HERO_BLOCK_ID} #{HERO_CARD_TEXT_EID} .c p{{
  text-align:center!important;line-height:1.45!important;font-size:clamp(14px,3.7vw,16px)!important}}
#{HERO_BLOCK_ID} #{HERO_BTN_EID}.gpc-e.e_botao,
#{HERO_BLOCK_ID} #{HERO_BTN_EID}.gpc-e.e_botao.berryup-cta-wrap-centered{{
  left:50%!important;transform:translateX(-50%)!important;
  width:min(277px,86vw)!important;max-width:86vw!important;
  height:auto!important;min-height:50px!important;z-index:1515!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_FOOTER_EID}{{
  left:50%!important;transform:translateX(-50%)!important;width:auto!important;
  max-width:min(300px,88vw)!important;text-align:center!important;z-index:1516!important;
  margin-top:0!important;padding-top:0!important}}
#{HERO_BLOCK_ID} #{HERO_CARD_FOOTER_EID} .c,
#{HERO_BLOCK_ID} #{HERO_CARD_FOOTER_EID} .c h4,
#{HERO_BLOCK_ID} #{HERO_CARD_FOOTER_EID} .c h4 span{{
  text-align:center!important;color:#242424!important}}
#{HERO_BLOCK_ID} #{HERO_ARROW_EID}{{
  left:50%!important;transform:translateX(-50%)!important;z-index:1511!important;
  width:auto!important;height:auto!important}}
}}
"""

CTA_SHAKE_MARKER_START = "/* berryup-cta-shake */"
CTA_SHAKE_MARKER_END = "/* /berryup-cta-shake */"

BERRYUP_CTA_SHAKE_CSS = """
@keyframes berryupCtaShake{
  0%,100%{translate:0 0;rotate:0deg}
  8%{translate:-3px 0;rotate:-1deg}
  16%{translate:3px 0;rotate:1deg}
  24%{translate:-3px 1px;rotate:-0.8deg}
  32%{translate:3px -1px;rotate:0.8deg}
  40%{translate:-2px 0;rotate:-0.5deg}
  48%{translate:2px 0;rotate:0.5deg}
  56%,100%{translate:0 0;rotate:0deg}
}
.gpc-e.e_botao:has(>.c>a.berryup-checkout-cta)>.c,
.gpc-e.e_botao:has(>.c>a.berryup-cta-pending)>.c,
.gpc-e.e_botao>a.berryup-checkout-cta,
.gpc-e.e_botao>a.berryup-cta-pending,
a.berryup-checkout-cta.berryup-cta-ready,
a.berryup-checkout-cta.berryup-cta-pending,
a.e_botao.berryup-checkout-cta.berryup-cta-ready,
a.e_botao.berryup-checkout-cta.berryup-cta-pending,
#berryup-ebook-oferta .beo-cta,
#berryup-roleta .br-cta-main.berryup-cta-ready,
#berryup-prize-bar .bpb-pay{
  animation:berryupCtaShake 2.4s ease-in-out infinite!important;
  transform-origin:center center}
#berryup-ebook-oferta .beo-cta,
a.berryup-checkout-cta,
a.e_botao.berryup-checkout-cta{
  transition:box-shadow .15s,filter .15s!important}
.gpc-e.e_botao:has(>.c>a.berryup-checkout-cta:hover)>.c,
.gpc-e.e_botao:has(>.c>a.berryup-cta-pending:hover)>.c,
.gpc-e.e_botao:has(>a.berryup-checkout-cta:hover),
.gpc-e.e_botao:has(>a.berryup-cta-pending:hover),
.gpc-e.e_botao>.c:has(>a.berryup-checkout-cta:hover),
.gpc-e.e_botao>.c:has(>a.berryup-cta-pending:hover),
a.berryup-checkout-cta.berryup-cta-ready:hover,
a.berryup-checkout-cta.berryup-cta-pending:hover,
a.e_botao.berryup-checkout-cta:hover,
#berryup-ebook-oferta .beo-cta:hover,
#berryup-roleta .br-cta-main.berryup-cta-ready:hover,
#berryup-prize-bar .bpb-pay:hover{
  animation:none!important}
@media(prefers-reduced-motion:reduce){
.gpc-e.e_botao:has(>.c>a.berryup-checkout-cta)>.c,
.gpc-e.e_botao:has(>.c>a.berryup-cta-pending)>.c,
.gpc-e.e_botao>a.berryup-checkout-cta,
.gpc-e.e_botao>a.berryup-cta-pending,
a.berryup-checkout-cta.berryup-cta-ready,
a.berryup-checkout-cta.berryup-cta-pending,
#berryup-ebook-oferta .beo-cta,
#berryup-roleta .br-cta-main.berryup-cta-ready,
#berryup-prize-bar .bpb-pay{
  animation:none!important}}
"""

WHEEL_SLICES = (
    {"pct": 60, "featured": True},
    {"pct": 40, "featured": False},
    {"pct": 10, "featured": False},
    {"pct": 20, "featured": False},
)

WHEEL_CSS = """
/* Roleta Berry Up */
#berryup-prize-bar{display:none;position:fixed;top:0;left:0;right:0;z-index:2100;background:#fff;color:#1a1030;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;border-bottom:3px solid #ff6316;box-shadow:0 4px 20px rgba(255,99,22,.18),0 2px 12px rgba(0,0,0,.08)}
body.berryup-wheel-won #berryup-prize-bar{display:block;animation:bpbSlideDown .35s ease}
@keyframes bpbSlideDown{from{transform:translateY(-100%);opacity:0}to{transform:translateY(0);opacity:1}}
body.berryup-wheel-won #site{padding-top:155px}
body.berryup-wheel-won #b_1002625_1_17307234956728bea7c7c12{display:none!important}
body.berryup-wheel-won #b_1002625_1_174828396566595021{
  position:relative!important;z-index:2095!important;height:auto!important;
  min-height:44px!important;overflow:visible!important}
body.berryup-wheel-won #b_1002625_1_174828396566595021 .centralizar{
  display:flex!important;align-items:center!important;justify-content:center!important;
  min-height:44px!important;height:auto!important;position:relative!important}
body.berryup-wheel-won #e_1002625_1_174828396566515887{
  position:relative!important;left:auto!important;top:auto!important;width:100%!important;
  max-width:100%!important;height:auto!important;transform:none!important}
body.berryup-wheel-won #e_1002625_1_174828396566515887 .c,
body.berryup-wheel-won #e_1002625_1_174828396566515887 .c p,
body.berryup-wheel-won #e_1002625_1_174828396566515887 .c span{
  line-height:1.25!important;font-size:clamp(13px,2.2vw,22px)!important;
  padding:10px 14px!important;text-align:center!important}
body.berryup-wheel-won.berryup-urgency-scrolled #site > *:not(#berryup-prize-bar){margin-top:0!important}
@media(max-width:800px){
#berryup-prize-bar{position:relative!important;top:auto!important;left:auto!important;right:auto!important;width:100%!important}
body.berryup-wheel-won #site{padding-top:0!important}
body.berryup-wheel-won #berryup-prize-bar{flex-shrink:0}
#berryup-prize-bar .bpb-inner{padding:12px 14px 14px!important}
}
#berryup-prize-bar .bpb-inner{
  max-width:1200px;margin:0 auto;padding:14px 22px;
  display:grid;grid-template-columns:auto minmax(0,1fr) auto auto;
  align-items:center;gap:14px 22px;font-size:1rem!important}
#berryup-prize-bar .bpb-alert-icon{
  flex-shrink:0;width:52px;height:52px;border-radius:50%;background:#fff3eb;border:2px solid #ff6316;
  display:flex;align-items:center;justify-content:center;font-size:1.45rem!important;line-height:1;grid-column:1}
#berryup-prize-bar .bpb-copy{
  grid-column:2;min-width:0;display:flex;flex-direction:column;gap:4px;text-align:left}
#berryup-prize-bar .bpb-kicker{
  display:block;font-size:clamp(.8rem,2vw,.92rem)!important;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;color:#ff6316}
#berryup-prize-bar .bpb-prize{
  display:block;font-weight:800;line-height:1.3;color:#1a1030!important;
  font-size:clamp(1.02rem,2.4vw,1.15rem)!important}
#berryup-prize-bar .bpb-prize strong{color:#ff6316;font-weight:900;font-size:1.08em}
#berryup-prize-bar .bpb-timer-wrap{
  grid-column:3;flex-shrink:0;display:flex;align-items:center;justify-content:center;padding:2px 0}
#berryup-prize-bar .bpb-countdown{
  display:flex;align-items:flex-end;justify-content:center;gap:clamp(6px,1.4vw,12px)}
#berryup-prize-bar .bpb-unit{
  display:flex;flex-direction:column;align-items:center;gap:clamp(5px,1vw,8px)}
#berryup-prize-bar .bpb-unit-val{
  display:flex;align-items:center;justify-content:center;
  width:clamp(58px,13vw,84px);min-width:clamp(58px,13vw,84px);
  height:clamp(58px,13vw,84px);
  background:#ff6316!important;color:#fff!important;border-radius:6px;
  font-size:clamp(2rem,5.8vw,3.05rem)!important;font-weight:800!important;line-height:1;
  font-variant-numeric:tabular-nums;letter-spacing:-.02em;
  box-shadow:0 4px 0 #d94e0a,0 8px 18px rgba(255,99,22,.32)}
#berryup-prize-bar .bpb-unit-lbl{
  font-size:clamp(.62rem,1.5vw,.72rem)!important;font-weight:800!important;
  letter-spacing:.1em;text-transform:uppercase;color:#ff6316!important;line-height:1}
#berryup-prize-bar .bpb-colon{
  color:#ff6316!important;font-weight:800!important;
  font-size:clamp(1.85rem,4.8vw,2.65rem)!important;line-height:1;
  padding-bottom:clamp(22px,5.5vw,30px)!important;user-select:none}
#berryup-prize-bar #berryup-prize-timer{display:none!important}
#berryup-prize-bar .bpb-pay{
  grid-column:4;display:inline-flex;align-items:center;justify-content:center;padding:14px 26px;
  background:linear-gradient(180deg,#fff86b,#fff133 55%,#ffd21c);color:#201713!important;text-decoration:none!important;
  border-radius:14px;font-weight:950;font-size:clamp(.95rem,2.6vw,1.05rem)!important;white-space:nowrap;
  box-shadow:0 6px 0 #bd7b00,0 12px 24px rgba(0,0,0,.2);text-transform:uppercase}
.bpb-pay:hover{filter:brightness(1.06);transform:translateY(-1px)}
@media(max-width:800px){
#berryup-prize-bar .bpb-inner{
  display:flex!important;flex-direction:column!important;flex-wrap:nowrap!important;
  align-items:stretch!important;justify-content:flex-start!important;
  padding:12px 14px 14px!important;gap:12px!important}
#berryup-prize-bar .bpb-alert-icon,
#berryup-prize-bar .bpb-copy,
#berryup-prize-bar .bpb-timer-wrap,
#berryup-prize-bar .bpb-pay{
  grid-column:unset!important;grid-row:unset!important;width:100%!important;max-width:100%!important}
#berryup-prize-bar .bpb-alert-icon{
  width:44px!important;height:44px!important;font-size:1.2rem!important;
  align-self:center!important;margin:0 auto!important;flex:0 0 auto!important;order:0!important}
#berryup-prize-bar .bpb-copy{
  flex:0 0 auto!important;order:1!important;text-align:center!important;gap:6px!important}
#berryup-prize-bar .bpb-kicker{line-height:1.25!important}
#berryup-prize-bar .bpb-prize{
  line-height:1.35!important;font-size:clamp(.95rem,4.2vw,1.08rem)!important}
#berryup-prize-bar .bpb-timer-wrap{
  order:2!important;flex:0 0 auto!important;
  display:flex!important;flex-direction:column!important;align-items:center!important;
  justify-content:center!important;padding:6px 0 2px!important;margin:0!important}
#berryup-prize-bar .bpb-countdown{
  width:100%!important;max-width:100%!important;justify-content:center!important;
  align-items:flex-end!important;gap:clamp(3px,1.2vw,8px)!important;flex-wrap:nowrap!important}
#berryup-prize-bar .bpb-unit-val{
  width:clamp(44px,12vw,56px)!important;min-width:clamp(44px,12vw,56px)!important;
  height:clamp(44px,12vw,56px)!important;font-size:clamp(1.45rem,7vw,1.9rem)!important}
#berryup-prize-bar .bpb-unit-lbl{font-size:clamp(.5rem,2.4vw,.58rem)!important}
#berryup-prize-bar .bpb-colon{
  font-size:clamp(1.25rem,5vw,1.65rem)!important;padding-bottom:clamp(14px,4vw,18px)!important}
#berryup-prize-bar .bpb-pay{
  order:3!important;flex:0 0 auto!important;width:100%!important;max-width:none!important;
  white-space:normal!important;text-align:center!important;line-height:1.25!important;padding:14px 18px!important}
#berryup-roleta{padding:24px 12px 32px!important}
#berryup-roleta .br-main{grid-template-columns:1fr;gap:20px}
#berryup-roleta .br-offer{max-width:100%!important;padding:20px 16px}
.br-wheel-wrap{width:min(300px,88vw)!important}
}
#berryup-roleta{background:linear-gradient(165deg,#1a1030 0%,#120a22 42%,#ff6316 150%);padding:36px 18px 48px;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#fff;position:relative;z-index:100}
#berryup-roleta .br-wrap{max-width:1080px;margin:0 auto}
#berryup-roleta .br-tag{margin:0 0 10px;font-size:.72rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#ffb347;text-align:center}
#berryup-roleta .br-title{margin:0 0 28px;font-size:clamp(1.4rem,4.2vw,2.05rem);font-weight:800;text-align:center;line-height:1.2}
#berryup-roleta .br-main{display:grid;grid-template-columns:minmax(280px,1fr) minmax(300px,1.05fr);gap:32px 40px;align-items:center}
@media(max-width:800px){#berryup-roleta .br-main{grid-template-columns:1fr;gap:20px;justify-items:center;text-align:center}}
.br-wheel-col{display:flex;flex-direction:column;align-items:center;gap:16px;width:100%;max-width:380px}
.br-wheel-wrap{position:relative;width:min(360px,94vw);aspect-ratio:1;filter:drop-shadow(0 16px 40px rgba(0,0,0,.4));overflow:hidden;border-radius:50%}
.br-pointer{position:absolute;top:-8px;left:50%;transform:translateX(-50%);width:0;height:0;border-left:14px solid transparent;border-right:14px solid transparent;border-top:22px solid #38bdf8;z-index:8;filter:drop-shadow(0 3px 6px rgba(0,0,0,.45))}
.br-wheel-rotor{position:absolute;inset:0;border-radius:50%;transition:none  /* JS requestAnimationFrame slow-stop drama */;will-change:transform;overflow:hidden;z-index:2}
.br-wheel-rotor.is-spinning{transition:transform 4.2s cubic-bezier(.12,.8,.15,1)}
.br-wheel-face{position:absolute;inset:0;border-radius:50%;z-index:1;background:conic-gradient(from -90deg,#ff6316 0deg 90deg,#7c3aed 90deg 180deg,#1e3a5f 180deg 270deg,#14b8a6 270deg 360deg);box-shadow:inset 0 0 0 7px rgba(255,255,255,.18)}
.br-wheel-face::after{content:"";position:absolute;inset:8%;border-radius:50%;z-index:1;background:conic-gradient(from -90deg,transparent 0deg 89.2deg,rgba(255,255,255,.45) 89.2deg 90.8deg,transparent 90.8deg 179.2deg,rgba(255,255,255,.45) 179.2deg 180.8deg,transparent 180.8deg 269.2deg,rgba(255,255,255,.45) 269.2deg 270.8deg,transparent 270.8deg 359.2deg,rgba(255,255,255,.45) 359.2deg 360deg);pointer-events:none}
.br-wheel-svg{position:absolute;inset:0;width:100%;height:100%;z-index:4;pointer-events:none}
.br-wheel-svg .br-wlbl{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-weight:800;fill:#fff!important}
.br-wheel-svg .br-wlbl-pct{font-size:22px;font-weight:900;fill:#fff!important}
.br-wheel-svg .br-wlbl-off{font-size:9px;font-weight:800;letter-spacing:.16em;fill:#fff!important;opacity:.92}
.br-wheel-svg .br-wlbl--max .br-wlbl-pct{font-size:24px;fill:#ffb347!important}
.br-hub{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:24%;aspect-ratio:1;border-radius:50%;background:linear-gradient(180deg,#fff 0%,#f0f0f0 100%);border:5px solid #1a1030;display:flex;align-items:center;justify-content:center;z-index:7;box-shadow:0 6px 24px rgba(0,0,0,.35)}
.br-spin-btn{width:100%;height:100%;border:0;border-radius:50%;background:transparent;color:#ff6316!important;font-weight:900;font-size:clamp(.8rem,3.2vw,1.02rem)!important;cursor:pointer;letter-spacing:.06em;text-transform:uppercase;text-shadow:none}
.br-spin-btn:disabled{opacity:.45;cursor:not-allowed;color:#6b7280!important}
.br-result{margin:0;padding:8px 14px;background:rgba(255,255,255,.08);border-radius:999px;font-size:.86rem;font-weight:600;min-height:1.2em;text-align:center;max-width:100%}
.br-offer{background:#fff;border-radius:20px;padding:26px 24px;color:#1a1030;box-shadow:0 24px 56px rgba(0,0,0,.28);width:100%;max-width:420px;box-sizing:border-box}
.br-offer h2{margin:0 0 12px;font-size:clamp(1.15rem,3.6vw,1.5rem);line-height:1.28;font-weight:800}
.br-offer>p{margin:0 0 18px;font-size:.94rem;color:#4b5563;line-height:1.5}
.br-steps{margin:0 0 18px;padding:0;list-style:none;display:flex;flex-direction:column;gap:10px}
.br-steps li{display:flex;align-items:flex-start;gap:10px;font-size:.88rem;color:#374151;line-height:1.4;text-align:left}
.br-steps li::before{content:attr(data-step);flex-shrink:0;width:22px;height:22px;border-radius:50%;background:#ff6316;color:#fff;font-size:.72rem;font-weight:800;display:flex;align-items:center;justify-content:center}
@media(max-width:900px){.br-steps li{text-align:center;flex-direction:column;align-items:center}}
.br-offer-won .br-prize-box{background:linear-gradient(135deg,#2d1b4e 0%,#1a1030 100%);color:#fff;border-radius:14px;padding:18px 16px;margin-bottom:16px;text-align:center}
.br-offer-won .br-prize-box .br-kicker{font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;opacity:.88;margin:0 0 8px}
.br-offer-won .br-price{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:center;gap:6px 14px;margin:0}
.br-offer-won .br-price .old{font-size:1rem;text-decoration:line-through;opacity:.65}
.br-offer-won .br-price .now{font-size:clamp(1.9rem,6vw,2.2rem);font-weight:900;color:#ffb347;line-height:1}
.br-offer-won .br-save{margin:10px 0 0;font-size:.86rem;opacity:.92;line-height:1.4}
.br-timer-row{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:6px;background:#f0f9ff;border-radius:12px;padding:12px 14px;margin-bottom:16px;font-size:.88rem;font-weight:700;color:#0c4a6e}
.br-timer-row #berryup-wheel-timer{font-variant-numeric:tabular-nums;color:#0284c7;font-size:1.05rem}
.br-cta-main{display:flex;align-items:center;justify-content:center;width:100%;padding:16px 20px;border:0;border-radius:14px;background:linear-gradient(180deg,#ff7a35,#ff6316);color:#fff!important;text-decoration:none!important;font-weight:800;font-size:clamp(.95rem,2.8vw,1.05rem);text-align:center;cursor:pointer;box-shadow:0 6px 0 #d94e0a,0 12px 28px rgba(255,99,22,.38);line-height:1.25;box-sizing:border-box}
.br-cta-main:hover{filter:brightness(1.05)}
.br-cta-main:disabled{opacity:.55;cursor:not-allowed;box-shadow:none;filter:none}
.br-cta-hint{font-size:.8rem;color:#6b7280;margin:12px 0 0;text-align:center;line-height:1.4}
.br-trust{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 14px;margin-top:14px;padding-top:14px;border-top:1px solid #e5e7eb;font-size:.75rem;color:#6b7280;font-weight:600}
.br-trust span{white-space:nowrap}
body:not(.berryup-wheel-won) a.berryup-cta-pending,
body:not(.berryup-wheel-won) .e_botao a.link_interno{position:relative}
body:not(.berryup-wheel-won) .berryup-cta-pending::after{content:"↑ Gire a roleta primeiro";position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);background:#1a1030;color:#ffb347;font-size:.65rem;font-weight:800;padding:5px 12px;border-radius:8px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .2s;z-index:50}
body:not(.berryup-wheel-won) .berryup-cta-pending:hover::after{opacity:1}
#berryup-roleta.berryup-roleta-highlight{animation:berryupRoletaPulse 1.2s ease 2}
@keyframes berryupRoletaPulse{0%,100%{box-shadow:inset 0 0 0 0 rgba(255,179,71,0)}50%{box-shadow:inset 0 0 0 4px rgba(255,179,71,.25)}}

/* Modal — desconto liberado (fecha com Ok, entendi) */
#berryup-win-modal{
  position:fixed;inset:0;z-index:22000;display:flex;align-items:center;justify-content:center;
  padding:max(16px,env(safe-area-inset-top,0px)) 16px max(16px,env(safe-area-inset-bottom,0px));
  opacity:0;visibility:hidden;pointer-events:none;transition:opacity .28s ease,visibility .28s ease}
#berryup-win-modal.is-open{opacity:1;visibility:visible;pointer-events:auto}
body.berryup-win-modal-open{overflow:hidden}
#berryup-win-modal .berryup-win-modal__backdrop{
  position:absolute;inset:0;background:rgba(12,8,24,.78);border:0;cursor:pointer}
#berryup-win-modal .berryup-win-modal__panel{
  position:relative;z-index:1;width:min(100%,400px);background:#fff;color:#1a1030;
  border-radius:20px;padding:28px 24px 24px;text-align:center;
  box-shadow:0 24px 64px rgba(0,0,0,.35);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
#berryup-win-modal .berryup-win-modal__panel h2{
  margin:0 0 10px;font-size:clamp(1.25rem,4.5vw,1.55rem);line-height:1.25;font-weight:800}
#berryup-win-modal .berryup-win-modal__panel p{
  margin:0 0 20px;font-size:clamp(.95rem,3.2vw,1.05rem);line-height:1.45;color:#4b5563}
#berryup-win-modal .berryup-win-modal__panel p strong{color:#ff6316}
#berryup-win-modal .berryup-win-modal__btn{
  display:inline-flex;align-items:center;justify-content:center;width:100%;min-height:52px;
  padding:14px 22px;border:0;border-radius:999px;background:#FFF133;color:#1a1a1a!important;
  font-weight:800;font-size:clamp(1rem,3.4vw,1.12rem);cursor:pointer;
  box-shadow:0 4px 14px rgba(0,0,0,.12)}
#berryup-win-modal .berryup-win-modal__btn:hover{filter:brightness(1.03)}

/* === Confetti burst celebration on 60% win === */
@keyframes confettiFall{
  0%{opacity:1;transform:translate(var(--cx),var(--cy)) rotate(0deg) scale(1)}
  100%{opacity:0;transform:translate(var(--ex),var(--ey)) rotate(var(--rot)) scale(.25)}
}
.berryup-confetti{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:99999;overflow:hidden}
.berryup-confetti span{position:absolute;width:var(--w);height:var(--h);border-radius:var(--br);background:var(--bg);animation:confettiFall var(--dur) cubic-bezier(.25,.46,.45,.94) forwards}
""" + BERRYUP_CTA_YELLOW_CSS


def _slice_label_center(angle_from_top_deg: float, radius: float = 54) -> tuple[float, float]:
    """Centro geométrico da fatia (0° = topo, sentido horário = conic-gradient)."""
    rad = math.radians(angle_from_top_deg)
    cx, cy = 100.0, 100.0
    x = cx + radius * math.sin(rad)
    y = cy - radius * math.cos(rad)
    return round(x, 1), round(y, 1)


def _wheel_labels_svg() -> str:
    """Rótulos no centro de cada cor (bissetriz da fatia, não na divisória)."""
    # Ordem do conic-gradient: laranja → roxo → azul → verde-água (sentido horário a partir do topo)
    slots = (
        (60, *_slice_label_center(45), True),
        (40, *_slice_label_center(135), False),
        (10, *_slice_label_center(225), False),
        (20, *_slice_label_center(315), False),
    )
    parts = [
        '<svg class="br-wheel-svg" data-slices="centered-v2" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    ]
    for pct, x, y, featured in slots:
        cls = "br-wlbl br-wlbl--max" if featured else "br-wlbl"
        parts.append(
            f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" class="{cls}">'
            f'<tspan class="br-wlbl-pct" x="{x}" dy="-5">{pct}%</tspan>'
            f'<tspan class="br-wlbl-off" x="{x}" dy="13">OFF</tspan>'
            f"</text>"
        )
    parts.append("</svg>")
    return "".join(parts)


def win_modal_html() -> str:
    return f"""
<div id="{WIN_MODAL_ID}" class="berryup-win-modal" hidden aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="berryup-win-modal-title">
<button type="button" class="berryup-win-modal__backdrop" aria-label="Fechar aviso"></button>
<div class="berryup-win-modal__panel">
<h2 id="berryup-win-modal-title">🎉 Desconto liberado!</h2>
<p>Você ganhou <strong>{WHEEL_DISCOUNT}% OFF</strong> no e-book Berry Up. O desconto já está aplicado nos botões da página.</p>
<button type="button" class="berryup-win-modal__btn" id="berryup-win-modal-btn">Ok, entendi</button>
</div>
</div>
"""


def wheel_html(checkout: str) -> str:
    labels_svg = _wheel_labels_svg()
    return f"""
<section id="{WHEEL_ID}" class="berryup-roleta" aria-label="Roleta de desconto">
<div class="br-wrap">
<p class="br-tag">Oferta exclusiva · 1 giro por visita</p>
<h1 class="br-title" id="berryup-wheel-heading">Gire a roleta e descubra seu desconto no e-book!</h1>
<div class="br-main">
<div class="br-wheel-col">
<div class="br-wheel-wrap">
<div class="br-pointer" aria-hidden="true"></div>
<div class="br-wheel-rotor" id="berryup-wheel-disk" role="img" aria-label="Roleta de descontos: 60%, 40%, 10% e 20% de desconto">
<div class="br-wheel-face"></div>
{labels_svg}
</div>
<div class="br-hub"><button type="button" class="br-spin-btn" id="berryup-wheel-spin">GIRAR</button></div>
</div>
<p class="br-result" id="berryup-wheel-result">Toque em GIRAR — o ponteiro indica seu desconto</p>
</div>
<div class="br-offer" id="berryup-wheel-offer">
<h2 id="berryup-offer-title">Gire para liberar seu desconto</h2>
<p id="berryup-offer-text">A roleta pode parar em <strong>10%, 20%, 40% ou 60% OFF</strong>. Depois do giro, todos os botões da página abrem o checkout com o valor aplicado.</p>
<ol class="br-steps">
<li data-step="1">Clique em <strong>GIRAR</strong> no centro da roleta</li>
<li data-step="2">Veja em qual fatia o ponteiro parou</li>
<li data-step="3">Reclame o desconto e pague com segurança</li>
</ol>
<button type="button" class="br-cta-main" id="berryup-wheel-cta-pending" disabled>Gire a roleta para continuar</button>
<p class="br-cta-hint">O botão de pagamento libera após o giro</p>
<div class="br-trust"><span>🔒 Pagamento seguro</span><span>📱 Acesso imediato</span><span>✓ Garantia 7 dias</span></div>
</div>
</div>
</div>
</section>
<div id="berryup-prize-bar" role="banner" aria-hidden="true">
<div class="bpb-inner">
<span class="bpb-prize">🎉 <span id="berryup-prize-text">Você ganhou {WHEEL_DISCOUNT}% de desconto no e-book Berry Up!</span></span>
<span class="bpb-timer-wrap">Reclamar antes de: <span id="berryup-prize-timer">05:00</span></span>
<a class="bpb-pay" id="berryup-prize-pay" href="{checkout}" target="_blank" rel="noopener">GARANTIR MEU ACESSO AGORA</a>
</div>
</div>
"""


def wheel_script(checkout: str) -> str:
    discount = WHEEL_DISCOUNT
    timer_sec = WHEEL_TIMER_SEC
    wheel_id = WHEEL_ID
    return f"""<script id="berryup-wheel-script">(function(){{
var CHECKOUT="{checkout}";
var DISCOUNT={discount};
var EBOOK_LIST={EBOOK_LIST_PRICE};
var EBOOK_INST={EBOOK_INSTALLMENTS};
var TIMER_SEC={timer_sec};
var WHEEL_ID="{wheel_id}";
var SK_WON="{STORAGE_WON}";
var SK_EXP="{STORAGE_EXPIRES}";
var SK_MODAL_DISMISSED="{STORAGE_MODAL_DISMISSED}";
var WIN_MODAL_ID="{WIN_MODAL_ID}";
var HERO_BLOCK="b_1002625_1_173566432642604808";
var RESULT_BLOCK="{RESULT_CTA_BLOCK_ID}";
var BUY_BLOCK="{BUY_CTA_BLOCK_ID}";
var SEVEN_DAYS_BLOCK="{SEVEN_DAYS_CTA_BLOCK_ID}";
function ctaWonLabel(a){{
  if(a&&a.closest("#"+RESULT_BLOCK))return "EU QUERO ESTE RESULTADO";
  return "GARANTIR MEU ACESSO";
}}
function ctaWonHtml(a){{
  var label=ctaWonLabel(a);
  return '<span class="berryup-cta-tag">'+DISCOUNT+'% OFF LIBERADO</span><span class="berryup-cta-main">'+label+'</span><span class="berryup-cta-sub">Acesso imediato + checkout seguro</span>';
}}
function applyCtaWonContent(a){{
  if(!a||a.tagName!=="A")return;
  a.classList.add("berryup-cta-ready");
  a.innerHTML=ctaWonHtml(a);
  a.setAttribute("aria-label",DISCOUNT+"% de desconto. "+ctaWonLabel(a));
  a.style.textDecoration="none";
}}
var GUARANTEE_LAYOUTS=[
  ["{SEVEN_DAYS_CTA_BLOCK_ID}","{SEVEN_DAYS_BTN_EID}","{SEVEN_DAYS_FOOTER_EID}"],
  ["{RESULT_CTA_BLOCK_ID}","e_1002625_1_17307234956728bea7d90dd079644693","e_1002625_1_17307234956728bea7d9524815599139"],
  ["b_1002625_1_17307234956728bea7c7c31","e_1002625_1_17307234956728bea7cf683593344026","e_1002625_1_17307234956728bea7cf917054800283"]
];
function layoutGuaranteeFooters(){{
  GUARANTEE_LAYOUTS.forEach(function(row){{
    var block=document.getElementById(row[0]);
    if(!block)return;
    var btn=document.getElementById(row[1]);
    var foot=document.getElementById(row[2]);
    if(!btn||!foot)return;
    var host=block.querySelector(".centralizar")||block;
    var hr=host.getBoundingClientRect();
    var btnR=btn.getBoundingClientRect();
    var footEl=foot;
    var gap=14;
    var top=btnR.bottom-hr.top+gap;
    var left=btnR.left-hr.left+(btnR.width-footEl.offsetWidth)/2;
    foot.style.top=Math.round(top)+"px";
    foot.style.left=Math.round(Math.max(8,left))+"px";
    foot.style.transform="none";
    foot.style.zIndex="1520";
    foot.style.width="auto";
    foot.style.maxWidth=Math.min(btnR.width,hr.width-16)+"px";
    btn.style.zIndex="1518";
  }});
}}
function scheduleGuaranteeLayout(){{
  layoutGuaranteeFooters();
  requestAnimationFrame(layoutGuaranteeFooters);
  setTimeout(layoutGuaranteeFooters,80);
}}
var HERO_BOX_ID="{HERO_BOX_EID}";
var HERO_TEXT_ID="{HERO_CARD_TEXT_EID}";
var HERO_FOOT_ID="{HERO_CARD_FOOTER_EID}";
var HERO_BTN_ID="{HERO_BTN_EID}";
var HERO_IMG_ID="{HERO_IMG_EID}";
function setHeroPos(el,top){{
  if(!el)return;
  el.style.setProperty("left","50%","important");
  el.style.setProperty("transform","translateX(-50%)","important");
  el.style.setProperty("top",Math.round(top)+"px","important");
}}
function setHeroPosDesktop(el,top){{
  if(!el)return;
  el.style.setProperty("left","-132px","important");
  el.style.setProperty("transform","none","important");
  el.style.setProperty("top",Math.round(top)+"px","important");
}}
function layoutHeroHeadlinesDesktop(){{
  if(!window.matchMedia("(min-width:801px)").matches)return;
  var title=document.getElementById("{HERO_TITLE_EID}");
  var kicker=document.getElementById("{HERO_KICKER_EID}");
  var headline=document.getElementById("{HERO_HEADLINE_EID}");
  if(!title||!kicker||!headline)return;
  var top=108;
  setHeroPosDesktop(title,top);
  top+=Math.max(title.offsetHeight,56)+18;
  setHeroPosDesktop(kicker,top);
  kicker.style.setProperty("width","min(720px,52vw)","important");
  kicker.style.setProperty("max-width","min(720px,52vw)","important");
  top+=Math.max(kicker.offsetHeight,44)+26;
  setHeroPosDesktop(headline,top);
  headline.style.setProperty("width","min(720px,52vw)","important");
  headline.style.setProperty("max-width","min(720px,52vw)","important");
}}
function layoutHeroHeadlines(){{
  if(!window.matchMedia("(max-width:800px)").matches)return;
  var title=document.getElementById("{HERO_TITLE_EID}");
  var kicker=document.getElementById("{HERO_KICKER_EID}");
  var headline=document.getElementById("{HERO_HEADLINE_EID}");
  var img=document.getElementById(HERO_IMG_ID);
  if(!title||!kicker||!headline)return;
  var top=4;
  setHeroPos(title,top);
  top+=title.offsetHeight+2;
  setHeroPos(kicker,top);
  kicker.style.setProperty("width","min(94vw,420px)","important");
  kicker.style.setProperty("max-width","94vw","important");
  top+=kicker.offsetHeight+14;
  setHeroPos(headline,top);
  top+=headline.offsetHeight+34;
  if(img)setHeroPos(img,top);
}}
function layoutHeroCard(){{
  if(!window.matchMedia("(max-width:800px)").matches)return;
  var block=document.getElementById(HERO_BLOCK);
  var cen=block&&block.querySelector(".centralizar");
  var img=document.getElementById(HERO_IMG_ID);
  var box=document.getElementById(HERO_BOX_ID);
  var text=document.getElementById(HERO_TEXT_ID);
  var btn=document.getElementById(HERO_BTN_ID);
  var foot=document.getElementById(HERO_FOOT_ID);
  var arrow=document.getElementById("{HERO_ARROW_EID}");
  if(!block||!box||!text||!btn||!foot)return;
  block.classList.add("berryup-hero-layout-ready");
  var overlap=36;
  var cardTop;
  if(img&&img.offsetHeight>0){{
    cardTop=img.offsetTop+img.offsetHeight-overlap;
  }}else{{
    cardTop=parseFloat(getComputedStyle(box).top)||480;
  }}
  var cardTopPx=Math.round(cardTop);
  setHeroPos(box,cardTopPx);
  setHeroPos(text,cardTopPx+14);
  var textTop=cardTopPx+14;
  var textH=text.offsetHeight||72;
  var btnTop=textTop+textH+10;
  setHeroPos(btn,btnTop);
  btn.style.setProperty("z-index","1518","important");
  var btnH=btn.offsetHeight||(won()?64:52);
  var footTop=btnTop+btnH+6;
  setHeroPos(foot,footTop);
  foot.style.setProperty("z-index","1516","important");
  foot.style.setProperty("max-width","min(300px,88vw)","important");
  var footH=foot.offsetHeight||20;
  var stackBottom=footTop+footH;
  if(arrow){{
    setHeroPos(arrow,stackBottom+8);
    arrow.style.setProperty("z-index","1511","important");
    stackBottom+=arrow.offsetHeight||24;
  }}
  stackBottom+=12;
  var boxH=stackBottom-cardTopPx;
  box.style.setProperty("min-height",Math.max(160,boxH)+"px","important");
  box.style.setProperty("height",Math.max(160,boxH)+"px","important");
  var blockH=Math.max(
    img?img.offsetTop+img.offsetHeight+16:0,
    stackBottom+16
  );
  block.style.setProperty("min-height",blockH+"px","important");
  block.style.setProperty("height","auto","important");
  if(cen){{
    cen.style.setProperty("min-height",blockH+"px","important");
    cen.style.setProperty("height","auto","important");
  }}
}}
function scheduleHeroLayout(){{
  layoutHeroHeadlinesDesktop();
  layoutHeroHeadlines();
  layoutHeroCard();
  requestAnimationFrame(function(){{
    layoutHeroHeadlinesDesktop();
    layoutHeroHeadlines();
    layoutHeroCard();
  }});
  setTimeout(function(){{
    layoutHeroHeadlinesDesktop();
    layoutHeroHeadlines();
    layoutHeroCard();
  }},80);
  setTimeout(function(){{
    layoutHeroHeadlinesDesktop();
    layoutHeroHeadlines();
    layoutHeroCard();
  }},450);
}}
function syncPrizeBarOffset(){{
  var bar=document.getElementById("berryup-prize-bar");
  var site=document.getElementById("site");
  if(!bar||!site||!document.body.classList.contains("berryup-wheel-won"))return;
  if(window.matchMedia("(max-width:800px)").matches){{
    site.style.paddingTop="";
    return;
  }}
  site.style.paddingTop=bar.offsetHeight+"px";
}}
function schedulePrizeBarOffset(){{
  syncPrizeBarOffset();
  requestAnimationFrame(syncPrizeBarOffset);
  setTimeout(syncPrizeBarOffset,80);
  setTimeout(syncPrizeBarOffset,400);
}}
function centerCtaWrappers(){{
  document.querySelectorAll(".gpc-e.e_botao").forEach(function(el){{
    if(el.closest("#"+WHEEL_ID)||el.closest("#berryup-prize-bar")||el.closest("#"+HERO_BLOCK))return;
    if(el.id==="{HERO_BTN_EID}")return;
    if(el.id&&el.id.indexOf("{DEPOIMENTOS_NEXT_CTA_PREFIX}")===0)return;
    if(el.id==="{SEVEN_DAYS_BTN_EID}")return;
    var a=el.querySelector("a.berryup-checkout-cta.berryup-cta-ready");
    if(!a)return;
    el.classList.add("berryup-cta-wrap-centered");
  }});
}}
var disk=document.getElementById("berryup-wheel-disk");
var spinBtn=document.getElementById("berryup-wheel-spin");
var resultEl=document.getElementById("berryup-wheel-result");
var offerEl=document.getElementById("berryup-wheel-offer");
var prizeTimer=document.getElementById("berryup-prize-timer");
var wheelTimer=document.getElementById("berryup-wheel-timer");
var rotation=0;
var spinning=false;

function won(){{return localStorage.getItem(SK_WON)==="1";}}
function expiresAt(){{
  var v=parseInt(localStorage.getItem(SK_EXP)||"0",10);
  return isNaN(v)?0:v;
}}
function setWon(){{
  localStorage.setItem(SK_WON,"1");
  localStorage.setItem(SK_EXP,String(Date.now()+TIMER_SEC*1000));
}}
function fmt(sec){{
  sec=Math.max(0,Math.floor(sec));
  var m=Math.floor(sec/60),s=sec%60;
  return (m<10?"0":"")+m+":"+(s<10?"0":"")+s;
}}
function pad2(n){{n=Math.max(0,Math.floor(n));return (n<10?"0":"")+n;}}
function setPrizeCountdown(sec){{
  sec=Math.max(0,Math.floor(sec));
  var d=Math.floor(sec/86400);
  var h=Math.floor((sec%86400)/3600);
  var m=Math.floor((sec%3600)/60);
  var s=sec%60;
  var elD=document.getElementById("berryup-prize-timer-d");
  var elH=document.getElementById("berryup-prize-timer-h");
  var elM=document.getElementById("berryup-prize-timer-m");
  var elS=document.getElementById("berryup-prize-timer-s");
  if(elD)elD.textContent=pad2(d);
  if(elH)elH.textContent=pad2(h);
  if(elM)elM.textContent=pad2(m);
  if(elS)elS.textContent=pad2(s);
  if(prizeTimer)prizeTimer.textContent=pad2(m)+":"+pad2(s);
}}
function tickTimers(){{
  var left=(expiresAt()-Date.now())/1000;
  if(left<=0){{
    setPrizeCountdown(0);
    if(wheelTimer)wheelTimer.textContent="00:00";
    return;
  }}
  setPrizeCountdown(left);
  if(wheelTimer)wheelTimer.textContent=fmt(left);
}}
function scrollToWheel(){{
  var el=document.getElementById(WHEEL_ID);
  if(!el)return;
  el.classList.add("berryup-roleta-highlight");
  setTimeout(function(){{el.classList.remove("berryup-roleta-highlight");}},2600);
  el.scrollIntoView({{behavior:"smooth",block:"start"}});
}}
function markCheckoutAnchors(){{
  document.querySelectorAll('a[href*="seguro.peachup"], a[href*="pay.cakto"], .beo-cta').forEach(function(a){{
    if(a.closest("#"+WHEEL_ID))return;
    if(a.closest("#berryup-prize-bar"))return;
    a.classList.add("berryup-checkout-cta");
    if(!won())a.classList.add("berryup-cta-pending");
  }});
  document.querySelectorAll(".e_botao a").forEach(function(a){{
    if(a.closest("#"+WHEEL_ID))return;
    if(a.closest("#berryup-prize-bar"))return;
    a.classList.add("berryup-checkout-cta");
    if(!won())a.classList.add("berryup-cta-pending");
  }});
}}
function formatBrl(value){{
  var n=Math.max(0,Number(value));
  var parts=n.toFixed(2).split(".");
  return "R$ "+parts[0]+","+parts[1];
}}
function updateEbookOfertaPrice(discountPct){{
  var root=document.getElementById("berryup-ebook-oferta");
  if(!root)return;
  var oldEl=root.querySelector(".beo-price .old");
  var nowEl=root.querySelector(".beo-price .now");
  var instEl=root.querySelector(".beo-price .inst");
  if(!nowEl||!instEl)return;
  var pct=Math.max(0,Math.min(100,Number(discountPct)||0));
  var list=EBOOK_LIST;
  var now=list*(1-pct/100);
  var per=now/EBOOK_INST;
  nowEl.textContent=formatBrl(now);
  instEl.textContent="ou "+EBOOK_INST+"x de "+formatBrl(per);
  if(oldEl){{
    oldEl.textContent="De "+formatBrl(list);
    oldEl.style.display=pct>0?"":"none";
  }}
}}
function updateOfferPanel(){{
  if(!offerEl)return;
  offerEl.classList.add("br-offer-won");
  offerEl.innerHTML=
    '<h2>🎉 Você ganhou o desconto máximo!</h2>'+
    '<div class="br-prize-box"><p class="br-kicker">Prêmio desbloqueado na fatia '+DISCOUNT+'%</p>'+
    '<p class="br-price"><span class="old">De R$ 97,00</span> <span class="now">R$ 38,80</span></p>'+
    '<p class="br-save">'+DISCOUNT+'% OFF no e-book Berry Up · você economiza R$ 58,20</p></div>'+
    '<div class="br-timer-row"><span>Reclamar antes de:</span> <span id="berryup-wheel-timer">05:00</span></div>'+
    '<a class="br-cta-main berryup-cta-ready" href="'+CHECKOUT+'" target="_blank" rel="noopener">'+
    '<span class="berryup-cta-tag">'+DISCOUNT+'% OFF</span>'+
    '<span class="berryup-cta-main-text">GARANTIR MEU ACESSO</span><span class="berryup-cta-sub">Acesso imediato + checkout seguro</span></a>'+
    '<div class="br-trust"><span>🔒 Pagamento seguro</span><span>📱 Acesso imediato</span><span>✓ Garantia 7 dias</span></div>';
  wheelTimer=document.getElementById("berryup-wheel-timer");
}}
function applyWonUI(){{
  document.body.classList.add("berryup-wheel-won");
  var bar=document.getElementById("berryup-prize-bar");
  if(bar)bar.setAttribute("aria-hidden","false");
  var h=document.getElementById("berryup-wheel-heading");
  if(h)h.textContent="Parabéns! Você ganhou "+DISCOUNT+"% de desconto!";
  if(resultEl)resultEl.textContent="🎯 Parou em "+DISCOUNT+"% OFF — desconto máximo!";
  if(spinBtn){{
    spinBtn.disabled=false;
    spinBtn.textContent="Ok, entendi";
    spinBtn.setAttribute("aria-label","Fechar aviso de desconto liberado");
  }}
  updateOfferPanel();
  updateEbookOfertaPrice(DISCOUNT);
  createConfetti();
  showWinModal();
  document.querySelectorAll(".berryup-checkout-cta").forEach(function(a){{
    if(a.closest("#berryup-prize-bar"))return;
    a.classList.remove("berryup-cta-pending");
    a.setAttribute("href",CHECKOUT);
    a.setAttribute("target","_blank");
    a.setAttribute("rel","noopener");
    applyCtaWonContent(a);
  }});
  centerCtaWrappers();
  scheduleGuaranteeLayout();
  scheduleHeroLayout();
  schedulePrizeBarOffset();
  document.querySelectorAll(".e_botao a").forEach(function(a){{
    a.classList.remove("link_interno");
    a.removeAttribute("data-bloco");
    a.removeAttribute("data-bloco-mobile");
  }});
  var pay=document.getElementById("berryup-prize-pay");
  if(pay){{
    pay.setAttribute("href",CHECKOUT);
    pay.textContent="GARANTIR MEU ACESSO AGORA";
  }}
  tickTimers();
}}
function createConfetti(){{
  var container=document.createElement("div");
  container.className="berryup-confetti";
  document.body.appendChild(container);
  var colors=["#ff6316","#FFD700","#FF1493","#00E5FF","#7CFC00","#FF6B6B","#a855f7","#FFF133"];
  var cx=window.innerWidth/2,cy=window.innerHeight/2;
  for(var i=0;i<120;i++){{
    var el=document.createElement("span");
    var angle=Math.random()*Math.PI*2;
    var dist=200+Math.random()*500;
    var ex=Math.cos(angle)*dist;
    var ey=Math.sin(angle)*dist-100;
    var w=6+Math.random()*8;
    var h=4+Math.random()*10;
    var rot=Math.random()*1080-540;
    var dur=1.2+Math.random()*1.8;
    var bg=colors[Math.floor(Math.random()*colors.length)];
    var br=Math.random()>.5?"50%":"2px";
    el.style.cssText="--cx:"+(-ex/2)+"px;--cy:"+(-ey/2)+"px;--ex:"+ex+"px;--ey:"+ey+"px;--rot:"+rot+"deg;--w:"+w+"px;--h:"+h+"px;--dur:"+dur+"s;--br:"+br+";--bg:"+bg+";left:"+cx+"px;top:"+cy+"px";
    container.appendChild(el);
  }}
  setTimeout(function(){{container.remove();}},4000);
}}
function modalDismissed(){{
  try{{return sessionStorage.getItem(SK_MODAL_DISMISSED)==="1";}}catch(e){{return false;}}
}}
function closeWinModal(){{
  var modal=document.getElementById(WIN_MODAL_ID);
  if(!modal)return;
  modal.classList.remove("is-open");
  modal.setAttribute("aria-hidden","true");
  modal.setAttribute("hidden","");
  document.body.classList.remove("berryup-win-modal-open");
  try{{sessionStorage.setItem(SK_MODAL_DISMISSED,"1");}}catch(e){{}}
}}
function showWinModal(){{
  if(modalDismissed())return;
  var modal=document.getElementById(WIN_MODAL_ID);
  if(!modal)return;
  modal.removeAttribute("hidden");
  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden","false");
  document.body.classList.add("berryup-win-modal-open");
  var btn=document.getElementById("berryup-win-modal-btn");
  if(btn)btn.focus();
}}
function bindWinModal(){{
  var modal=document.getElementById(WIN_MODAL_ID);
  if(!modal||modal.getAttribute("data-bound")==="1")return;
  modal.setAttribute("data-bound","1");
  var btn=document.getElementById("berryup-win-modal-btn");
  var backdrop=modal.querySelector(".berryup-win-modal__backdrop");
  if(btn)btn.addEventListener("click",closeWinModal);
  if(backdrop)backdrop.addEventListener("click",closeWinModal);
  document.addEventListener("keydown",function(e){{
    if(e.key==="Escape"&&modal.classList.contains("is-open"))closeWinModal();
  }});
}}

function onSpinBtnClick(e){{
  if(won()){{
    if(e){{e.preventDefault();e.stopPropagation();}}
    closeWinModal();
    return;
  }}
  onSpin();
}}
function onSpin(){{
  if(spinning||won()||!disk||!spinBtn)return;
  spinning=true;
  spinBtn.disabled=true;
  disk.classList.add("is-spinning");
  if(resultEl)resultEl.textContent="Girando… boa sorte!";
  var turns=7;
  rotation+=360*turns;
  disk.style.transform="rotate("+rotation+"deg)";
  setTimeout(function(){{
    spinning=false;
    setWon();
    applyWonUI();
    markCheckoutAnchors();
  }},4200);
}}
function onDocClick(e){{
  if(won())return;
  var t=e.target;
  var anchor=t.closest("a");
  var inWheel=t.closest("#"+WHEEL_ID);
  var inBar=t.closest("#berryup-prize-bar");
  if(inWheel||inBar)return;
  var href=anchor&&anchor.getAttribute("href")||"";
  var isCheckout=anchor&&(anchor.classList.contains("berryup-checkout-cta")||href.indexOf("seguro.peachup")>=0||href.indexOf("pay.cakto")>=0);
  var isBtn=t.closest(".e_botao");
  if(isCheckout)return;
  if(isBtn){{
    e.preventDefault();
    e.stopPropagation();
    scrollToWheel();
  }}
}}
function init(){{
  updateEbookOfertaPrice(won()?DISCOUNT:0);
  markCheckoutAnchors();
  window.addEventListener("resize",function(){{
    scheduleHeroLayout();
    if(won()){{
      scheduleGuaranteeLayout();
      schedulePrizeBarOffset();
    }}
  }});
  if(window.matchMedia("(max-width:800px)").matches){{
    scheduleHeroLayout();
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(scheduleHeroLayout);
  }}
  bindWinModal();
  if(won()){{
    applyWonUI();
    schedulePrizeBarOffset();
    setInterval(tickTimers,1000);
    tickTimers();
    return;
  }}
  document.addEventListener("click",onDocClick,true);
  if(spinBtn)spinBtn.addEventListener("click",onSpinBtnClick);
}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);
else init();
}})();</script>"""


def _remove_tag_block(html: str, tag: str, element_id: str) -> str:
    start = html.find(f'<{tag} id="{element_id}"')
    if start < 0:
        return html
    if tag == "div":
        depth = 0
        i = start
        open_tag = "<div"
        close_tag = "</div>"
        while i < len(html):
            if html.startswith(open_tag, i):
                depth += 1
                i += len(open_tag)
                continue
            if html.startswith(close_tag, i):
                depth -= 1
                i += len(close_tag)
                if depth == 0:
                    return html[:start] + html[i:]
                continue
            i += 1
        return html
    end = html.find(f"</{tag}>", start)
    if end < 0:
        return html
    return html[:start] + html[end + len(f"</{tag}>") :]


def _remove_wheel_script(html: str) -> str:
    start = html.find(f'<script id="{WHEEL_SCRIPT_ID}">')
    if start < 0:
        return html
    end = html.find("</script>", start)
    if end < 0:
        return html
    return html[:start] + html[end + len("</script>") :]


def _strip_wheel_from_html(html: str) -> str:
    """Remove roleta, barra de prêmio e script para reinserir na posição correta."""
    html = _remove_tag_block(html, "section", WHEEL_ID)
    html = _remove_tag_block(html, "div", PRIZE_BAR_ID)
    html = _remove_wheel_script(html)
    return html


def _block_end(html: str, block_id: str) -> int:
    """Índice após o </div> de fechamento do bloco gpc-b."""
    start = html.find(f'<div id="{block_id}"')
    if start < 0:
        return -1
    depth = 0
    i = start
    open_tag = "<div"
    close_tag = "</div>"
    while i < len(html):
        if html.startswith(open_tag, i):
            depth += 1
            i += len(open_tag)
            continue
        if html.startswith(close_tag, i):
            depth -= 1
            i += len(close_tag)
            if depth == 0:
                return i
            continue
        i += 1
    return -1


def _insert_after_block(html: str, block_id: str, snippet: str) -> str:
    end = _block_end(html, block_id)
    if end < 0:
        return html + snippet
    return html[:end] + snippet + html[end:]


def prize_bar_html(checkout: str) -> str:
    return f"""
<div id="{PRIZE_BAR_ID}" class="bpb-alert" role="banner" aria-hidden="true">
<div class="bpb-inner">
<span class="bpb-alert-icon" aria-hidden="true">🚨</span>
<div class="bpb-copy">
<span class="bpb-kicker">Desconto liberado — clique abaixo</span>
<span class="bpb-prize"><span id="berryup-prize-text">Você ganhou <strong>{WHEEL_DISCOUNT}% OFF</strong> no e-book Berry Up!</span></span>
</div>
<span class="bpb-timer-wrap" aria-label="Tempo para reclamar o desconto" role="timer">
<span class="bpb-countdown">
<span class="bpb-unit"><span class="bpb-unit-val" id="berryup-prize-timer-d">00</span><span class="bpb-unit-lbl">DIAS</span></span>
<span class="bpb-colon" aria-hidden="true">:</span>
<span class="bpb-unit"><span class="bpb-unit-val" id="berryup-prize-timer-h">00</span><span class="bpb-unit-lbl">HORAS</span></span>
<span class="bpb-colon" aria-hidden="true">:</span>
<span class="bpb-unit"><span class="bpb-unit-val" id="berryup-prize-timer-m">05</span><span class="bpb-unit-lbl">MINUTOS</span></span>
<span class="bpb-colon" aria-hidden="true">:</span>
<span class="bpb-unit"><span class="bpb-unit-val" id="berryup-prize-timer-s">00</span><span class="bpb-unit-lbl">SEGUNDOS</span></span>
</span>
<span id="berryup-prize-timer" hidden>05:00</span>
</span>
<a class="bpb-pay" id="berryup-prize-pay" href="{checkout}" target="_blank" rel="noopener">GARANTIR MEU ACESSO AGORA</a>
</div>
</div>
"""


def wheel_section_html(checkout: str) -> str:
    """Só a seção da roleta (sem barra fixa)."""
    full = wheel_html(checkout)
    bar_start = full.find(f'<div id="{PRIZE_BAR_ID}"')
    return full[:bar_start].strip() + "\n"


def _fix_empty_site_wrapper(html: str) -> str:
    """Só corrige #site vazio; não mexe em mais nada do DOM."""
    return html.replace('<div id="site">\n\n\n</div>\n', '<div id="site">\n', 1)


def _wheel_is_after_hero(html: str) -> bool:
    hero = html.find(f'<div id="{HERO_BLOCK_ID}"')
    wheel = html.find(f'<section id="{WHEEL_ID}"')
    if hero < 0 or wheel < 0:
        return False
    hero_end = _block_end(html, HERO_BLOCK_ID)
    if hero_end < 0:
        return False
    nxt = re.search(r'<div id="b_[^"]+"', html[hero_end:])
    next_start = hero_end + nxt.start() if nxt else len(html)
    return hero_end <= wheel < next_start


def _wheel_needs_refresh(html: str) -> bool:
    """Reinjeta se a roleta ainda usa markup/CSS antigo."""
    return (
        'class="br-wheel-rotor"' not in html
        or 'data-slices="centered-v2"' not in html
    )


def _upsert_wheel_css(html: str) -> str:
    marker = "/* Roleta Berry Up */"
    start = html.find(marker)
    if start >= 0:
        kf = html.find("@keyframes berryupRoletaPulse", start)
        if kf >= 0:
            end = html.find("}", kf) + 1
            html = html[:start] + html[end:]
    return html.replace("</style>", WHEEL_CSS + "</style>", 1)


def _upsert_cta_shake_css(html: str) -> str:
    """Tremor nos CTAs — injeta no fim do primeiro <style> para ganhar cascata."""
    while CTA_SHAKE_MARKER_START in html:
        start = html.find(CTA_SHAKE_MARKER_START)
        end = html.find(CTA_SHAKE_MARKER_END, start)
        if end < 0:
            html = html[:start] + html[start + len(CTA_SHAKE_MARKER_START) :]
            break
        end += len(CTA_SHAKE_MARKER_END)
        if end < len(html) and html[end] == "\n":
            end += 1
        html = html[:start] + html[end:]
    pos = html.find("</style>")
    if pos < 0:
        return html
    block = CTA_SHAKE_MARKER_START + BERRYUP_CTA_SHAKE_CSS + CTA_SHAKE_MARKER_END + "\n"
    return html[:pos] + block + html[pos:]


def inject_berryup_wheel(html: str, checkout: str) -> str:
    """Roleta logo abaixo do banner hero; barra de prêmio fixa no topo do #site."""
    if f'<div id="{HERO_BLOCK_ID}"' not in html:
        return html

    html = _fix_empty_site_wrapper(html)

    if not _wheel_is_after_hero(html) or _wheel_needs_refresh(html):
        html = _strip_wheel_from_html(html)
        bundle = wheel_section_html(checkout) + wheel_script(checkout)
        html = _insert_after_block(html, HERO_BLOCK_ID, bundle)

    site_marker = '<div id="site">'
    if site_marker in html:
        html = _remove_tag_block(html, "div", PRIZE_BAR_ID)
        html = html.replace(site_marker, site_marker + prize_bar_html(checkout), 1)

    html = _upsert_wheel_css(html)
    html = _upsert_cta_shake_css(html)
    html = _upsert_win_modal(html)
    return html


def _upsert_win_modal(html: str) -> str:
    if f'id="{WIN_MODAL_ID}"' in html:
        return html
    marker = "</body>"
    if marker not in html:
        return html
    return html.replace(marker, win_modal_html() + marker, 1)
