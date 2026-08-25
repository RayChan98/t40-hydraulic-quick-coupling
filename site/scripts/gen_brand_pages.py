# -*- coding: utf-8 -*-
"""S2 机器品牌矩阵生成器：品牌兼容快接页（ehhydraulics 模式，做深做准）"""
import os, re

BASE = r'D:\kravzik-work\t40-hydraulic-quick-coupling\site\src\pages'

TPL = '''---
import Layout from '../layouts/Layout.astro';
---
<Layout title="{brand} Hydraulic Quick Couplers | Hydraulic Quick Couplings" description="Hydraulic quick couplers for {brand} machines — ISO 7241 / ISO 16028 flat-face / ISO 5675 profiles, sizes, threads and selection notes for {brand} fleets.">
  <section class="bg-navy-950 text-white">
    <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6">
      <p class="text-sm font-semibold text-night-green">Machine-Compatible Quick Couplings</p>
      <h1 class="mt-2 max-w-3xl text-4xl font-extrabold tracking-tight">{brand} Hydraulic Quick Couplers</h1>
      <p class="mt-3 max-w-2xl text-lg text-slate-300">Source the right quick-disconnect couplings for {brand} machines — attachment lines, implement outlets and service replacements.</p>
    </div>
  </section>

  <section class="bg-white">
    <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6">
      <div class="prose prose-lg max-w-none prose-headings:font-extrabold prose-headings:text-navy-950 prose-h2:mt-10 prose-p:text-slate-600 prose-a:text-brand-blue">
        <h2>{brand} Machines and Their Hydraulic Quick Couplings</h2>
        <p>{intro}</p>
        <h2>Coupling Profiles You Will Find on {brand} Equipment</h2>
        <p>The table below summarises the quick-coupling profiles most commonly used across {brand} machine families. It is a field guide, not a guarantee: verify the profile on your specific machine before ordering.</p>
        <table>
          <thead><tr><th>Machine family</th><th>Common profile</th><th>Typical sizes</th><th>Typical threads</th></tr></thead>
          <tbody>
            <tr><td>{fam1}</td><td>{std1}</td><td>{size1}</td><td>{thr1}</td></tr>
            <tr><td>{fam2}</td><td>{std2}</td><td>{size2}</td><td>{thr2}</td></tr>
            <tr><td>{fam3}</td><td>{std3}</td><td>{size3}</td><td>{thr3}</td></tr>
          </tbody>
        </table>
        <h2>Selection Notes for {brand} Fleets</h2>
        <ul>
          {bullets}
        </ul>
        <h2>Replacement and Service Guidance</h2>
        <p>{service}</p>
        <h2>FAQ</h2>
        {faqhtml}
      </div>
    </div>
  </section>

  <section class="bg-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6">
      <div class="flex flex-col items-center justify-between gap-6 rounded-2xl bg-navy-950 p-8 text-center sm:p-10 lg:flex-row lg:text-left">
        <div>
          <h3 class="text-2xl font-extrabold text-white">Need Couplings for {brand} Machines?</h3>
          <p class="mt-2 text-slate-300">Send the machine model, coupling profile or a photo — we confirm the match within 24 hours.</p>
        </div>
        <a href="/contact/" class="rounded-lg bg-cta-orange px-6 py-3 font-semibold text-white transition hover:bg-orange-600">Request a Quote</a>
      </div>
    </div>
  </section>
</Layout>
'''

def esc(s):
    return s.replace('"', '&quot;')

def j(o):
    import json
    return json.dumps(o, ensure_ascii=False)

BRANDS = [
  dict(brand='Bobcat', slug='bobcat',
       intro="Bobcat skid steer loaders, compact track loaders and compact excavators are built around fast attachment changes. Their auxiliary hydraulic lines use flat-face quick couplings (ISO 16028 style) so operators can switch buckets, breakers, augers and grapples without spilling oil or letting dirt into the circuit. Flat-face design is the Bobcat norm on loader auxiliary lines; older or non-standard machines may carry ball-lock couplings, so always confirm before ordering.",
       fam1='Skid steer / CTL auxiliaries', std1='Flat-face (ISO 16028 style)', size1='1/2&quot; flat face; high-flow variants', thr1='NPT / ORFS',
       fam2='Compact excavator auxiliaries', std2='Flat-face (ISO 16028 style)', size2='3/8&quot; - 3/4&quot; flat face', thr2='ORFS / NPT',
       fam3='Older / service lines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Flat-face (ISO 16028 style) couplings are the safe choice for Bobcat loader lines: they minimise spill during attachment changes and keep contamination out of the hydraulic circuit.</li><li>Confirm the thread on the machine side — Bobcat machines in North America typically run NPT or ORFS ends; verify with the machine's parts list.</li><li>Dust caps and plugs protect the flat faces when attachments are disconnected; a scratched flat face is the most common cause of internal leakage.</li>",
       service="For service replacements, note the machine model and serial range, and whether the auxiliary line is standard flow or high flow. High-flow circuits need couplings rated for the higher flow and pressure. If in doubt, send a photo of the male and female halves — the flat-face profile is easy to confirm from a side view.",
       faqs=[['Are all Bobcat skid steer couplers flat-face?', "Most modern Bobcat loader auxiliary lines use flat-face (ISO 16028 style) couplings, but machine age, options and aftermarket retrofits vary. Check the coupling face — flat-face halves have a flush, flat sealing surface; ball-lock halves have a visible ball cage."],
             ['Can I replace Bobcat flat-face couplings with cheaper ball-lock ones?', "Physically the threads may match, but flat-face and ball-lock profiles do not mate. Replacing one half forces you to replace the matching half too — and you lose the spill/contamination benefits of flat-face. Standard practice is to keep the profile the machine was built with."],
             ['What sizes do Bobcat machines use?', 'Compact machines commonly use 1/2&quot; flat-face couplings on standard-flow auxiliary lines, with larger flat-face sizes on high-flow lines. Always confirm against the machine or its parts list.']]),
  dict(brand='Caterpillar', slug='caterpillar',
       intro="Caterpillar builds skid steers, compact track loaders, mini excavators and full-size excavators, plus a range of work tools that connect to auxiliary hydraulics. Modern Cat compact equipment uses flat-face quick couplings on auxiliary lines; older machines and certain applications carry ball-lock ISO 7241 couplings. Tractor-type applications follow ISO 5675 where applicable.",
       fam1='Skid steer / CTL auxiliaries', std1='Flat-face (ISO 16028 style)', size1='1/2&quot; flat face', thr1='NPT / ORFS',
       fam2='Excavator auxiliary lines', std2='Flat-face (ISO 16028 style)', size2='1/2&quot; - 3/4&quot;', thr2='ORFS / metric',
       fam3='Service / older machines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Cat compact loader and excavator auxiliary circuits are predominantly flat-face today — keep that profile when replacing couplings.</li><li>Verify the working pressure rating: heavy Cat work tools (breakers, high-flow mulchers) push circuits toward the upper end of flat-face ratings.</li><li>Thread ends differ by market: North American machines favour NPT/ORFS, while metric-thread machines appear in other regions.</li>",
       service="When ordering Cat-compatible couplings, provide the machine model, the auxiliary line flow (standard vs high flow) and a photo or part number of the existing coupling. Cat machines use a mix of profiles across model years, so model number alone is not enough to guarantee the profile.",
       faqs=[['Do Cat excavators use flat-face or ball-lock couplings?', 'Modern Cat excavator auxiliary lines are typically flat-face (ISO 16028 style). Some older machines and certain attachment kits use ball-lock ISO 7241 couplings. Check the coupling face before ordering.'],
             ['Is there a Cat-specific coupling standard?', 'Cat uses industry-standard profiles (ISO 16028 flat-face, ISO 7241 ball-lock, ISO 5675 agricultural) rather than a proprietary coupling standard, so standard-profile couplings can be sourced aftermarket.'],
             ['What about high-flow Cat machines?', 'High-flow auxiliary circuits need flat-face couplings rated for higher flow and pressure. Match the coupling size to the flow requirement, not just the hose diameter.']]),
  dict(brand='John Deere', slug='john-deere',
       intro="John Deere spans tractors, combines, sprayers and a full construction line (skid steers, compact track loaders, excavators). Agricultural tractors use ISO 5675 couplings on the rear SCV outlets for implements; construction equipment uses flat-face (ISO 16028 style) on auxiliary lines; older industrial machines may carry ISO 7241 ball-lock couplings.",
       fam1='Tractor rear SCV outlets', std1='ISO 5675 (agricultural)', size1='1/2&quot; ISO 5675', thr1='BSPP / NPT',
       fam2='Skid steer / CTL auxiliaries', std2='Flat-face (ISO 16028 style)', size2='1/2&quot; flat face', thr2='NPT / ORFS',
       fam3='Industrial / older lines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Deere tractor rear outlets are ISO 5675 — the agricultural profile with free-flow poppets for implement circuits.</li><li>Deere construction equipment moved to flat-face on loader auxiliaries; match the profile on replacements.</li><li>ISO 5675 couplings are not interchangeable with ISO 7241 or ISO 16028 — keep the families separate on the parts shelf.</li>",
       service="For Deere tractors, specify ISO 5675 for rear outlets and confirm the SCV thread (typically 1/2&quot; BSPP in Europe / NPT in North America). For Deere construction machines, specify flat-face for loader auxiliaries. Model + coupling photo removes all guesswork.",
       faqs=[['Do John Deere tractors use ISO 5675?', 'Yes — Deere tractor rear SCV outlets use ISO 5675 agricultural couplings (sometimes called "AG couplers"). They are the standard for tractor-to-implement hydraulic connections.'],
             ['What couplings do Deere skid steers use?', 'Modern Deere skid steers and compact track loaders use flat-face (ISO 16028 style) quick couplings on the auxiliary lines.'],
             ['Can I use one coupling type for everything on a Deere machine?', 'No — tractor rear outlets (ISO 5675), loader auxiliaries (flat-face) and any legacy ball-lock lines each need their own profile. Stock all three for full coverage.']]),
  dict(brand='Kubota', slug='kubota',
       intro="Kubota is one of the largest compact-equipment makers in the world — tractors, compact excavators, skid steers, utility vehicles and mowers. Kubota tractors use ISO 5675 couplings on rear outlets; compact excavators and loaders use flat-face (ISO 16028 style) on auxiliary lines; some models carry ball-lock ISO 7241 couplings on service lines.",
       fam1='Tractor rear outlets', std1='ISO 5675 (agricultural)', size1='1/2&quot; ISO 5675', thr1='BSPP / NPT',
       fam2='Excavator / loader auxiliaries', std2='Flat-face (ISO 16028 style)', size2='1/2&quot; flat face', thr2='NPT / ORFS / BSPP',
       fam3='Service lines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Kubota compact excavators and skid steers predominantly use flat-face couplings on auxiliary lines — the default replacement profile.</li><li>Kubota tractor rear outlets are ISO 5675; confirm the outlet thread (BSPP is common outside North America).</li><li>Utility vehicle (RTV) hydraulic lines vary; check the coupling face and threads before ordering.</li>",
       service="Kubota machines are sold worldwide with different thread conventions by market. Always specify the market/region with the model, because a Kubota L-series tractor in Europe (BSPP outlets) differs from the same model in North America (often NPT).",
       faqs=[['Are Kubota tractor outlets ISO 5675?', 'Yes, Kubota tractor rear hydraulic outlets use ISO 5675 agricultural couplings, standard across the tractor industry.'],
             ['What couplings do Kubota excavators use?', 'Kubota compact excavators use flat-face (ISO 16028 style) couplings on auxiliary lines, with 1/2&quot; as the most common size.'],
             ['Are Kubota couplings proprietary?', 'Kubota uses industry-standard profiles (ISO 5675, ISO 16028, ISO 7241), so standard couplings can be sourced from any supplier.']]),
  dict(brand='Case', slug='case',
       intro="Case (Case IH agriculture and Case Construction) builds tractors, combines, skid steers, compact track loaders and excavators. Case IH tractor rear outlets use ISO 5675; Case Construction skid steers and excavators use flat-face (ISO 16028 style) on auxiliary lines; older machines may carry ISO 7241 ball-lock couplings.",
       fam1='Tractor rear outlets', std1='ISO 5675 (agricultural)', size1='1/2&quot; ISO 5675', thr1='BSPP / NPT',
       fam2='Skid steer / CTL auxiliaries', std2='Flat-face (ISO 16028 style)', size2='1/2&quot; flat face', thr2='NPT / ORFS',
       fam3='Excavator / older lines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Case IH tractor outlets are ISO 5675 — match with agricultural-profile couplings and seals.</li><li>Case skid steer and CTL loader auxiliaries use flat-face; keep the profile on replacements.</li><li>Check the thread per market: North American machines favour NPT/ORFS; export machines vary.</li>",
       service="Provide the machine model and the coupling face type (flat-face vs ball-lock) for Case machines. Case IH implements may specify ISO 5675 outlet size and thread — confirm both ends.",
       faqs=[['Do Case IH tractors use ISO 5675?', 'Yes — Case IH tractor rear outlets use ISO 5675 agricultural couplings.'],
             ['What do Case skid steers use?', 'Case skid steers and CTLs use flat-face (ISO 16028 style) couplings on auxiliary hydraulic lines.'],
             ['Are Case and New Holland couplings the same?', 'Both are CNH brands and both follow industry standards (ISO 5675, ISO 16028). Profiles are standard; always verify per machine model.']]),
  dict(brand='New Holland', slug='new-holland',
       intro="New Holland (CNH) covers tractors, combines, telehandlers, skid steers and backhoe loaders. Tractor rear outlets use ISO 5675; skid steers and compact equipment use flat-face (ISO 16028 style); backhoe and older industrial lines may carry ISO 7241 ball-lock couplings.",
       fam1='Tractor rear outlets', std1='ISO 5675 (agricultural)', size1='1/2&quot; ISO 5675', thr1='BSPP / NPT',
       fam2='Skid steer / CTL auxiliaries', std2='Flat-face (ISO 16028 style)', size2='1/2&quot; flat face', thr2='NPT / ORFS',
       fam3='Backhoe / service lines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>New Holland tractor outlets are ISO 5675 — the industry agricultural profile.</li><li>New Holland skid steers use flat-face loader auxiliaries; match profile on replacements.</li><li>Telehandler auxiliary lines may be flat-face or ball-lock depending on model year — verify before ordering.</li>",
       service="For New Holland telehandlers, the auxiliary coupling profile changed across model years. Send the machine model, serial range and a photo of the existing coupling to avoid ordering the wrong family.",
       faqs=[['Do New Holland tractors use ISO 5675?', 'Yes — New Holland tractor rear outlets are ISO 5675 agricultural couplings.'],
             ['What do New Holland skid steers use?', 'New Holland skid steers use flat-face (ISO 16028 style) couplings on auxiliary lines.'],
             ['Why does my New Holland telehandler have different couplings than the tractor?', 'Telehandlers connect attachments with higher flow/pressure than tractor SCV outlets, so they typically use flat-face or larger ball-lock couplings rather than ISO 5675.']]),
  dict(brand='JCB', slug='jcb',
       intro="JCB builds backhoe loaders, telehandlers, excavators, skid steers and compact loaders. JCB machines use flat-face (ISO 16028 style) couplings on most modern auxiliary lines; older backhoes and certain attachments may carry ISO 7241 ball-lock couplings.",
       fam1='Telehandler auxiliaries', std1='Flat-face (ISO 16028 style)', size1='1/2&quot; - 3/4&quot;', thr1='ORFS / NPT / BSPP',
       fam2='Excavator auxiliary lines', std2='Flat-face (ISO 16028 style)', size2='1/2&quot; - 3/4&quot;', thr2='ORFS / metric',
       fam3='Older backhoe lines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Modern JCB machines use flat-face couplings on auxiliary lines — the standard for attachment changeover with low spill.</li><li>JCB backhoes built before the flat-face era may carry ball-lock couplings; confirm the face type.</li><li>Thread ends vary by export market; specify the region when ordering.</li>",
       service="JCB machines are highly configurable at the factory. Provide the machine model, build year and a photo of the coupling halves — JCB auxiliary kits vary by model and option.",
       faqs=[['Do JCB telehandlers use flat-face?', 'Most modern JCB telehandlers use flat-face (ISO 16028 style) couplings on auxiliary lines.'],
             ['Are old JCB backhoes flat-face?', 'Older JCB backhoes often carry ball-lock ISO 7241 couplings; newer models use flat-face. Check the coupling face.'],
             ['Can I retrofit a JCB machine to flat-face?', 'Yes — replace both halves on the hose and machine sides. It is a common upgrade that reduces spill and contamination.']]),
  dict(brand='Komatsu', slug='komatsu',
       intro="Komatsu is a global leader in excavators, wheel loaders, dozers and dump trucks. Modern Komatsu excavator auxiliary lines use flat-face (ISO 16028 style) couplings; older machines and certain models may use ISO 7241 ball-lock couplings. Wheel loader and dozer auxiliary circuits follow the same pattern.",
       fam1='Excavator auxiliaries', std1='Flat-face (ISO 16028 style)', size1='1/2&quot; - 3/4&quot;', thr1='ORFS / metric',
       fam2='Wheel loader auxiliaries', std2='Flat-face (ISO 16028 style)', size2='1/2&quot; - 3/4&quot;', thr2='ORFS / NPT',
       fam3='Older machines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Komatsu excavators use flat-face couplings on standard auxiliary lines; high-flow circuits need larger flat-face sizes.</li><li>Confirm the thread: Komatsu machines in Asia often use metric threads; export machines vary.</li><li>Older Komatsu machines (pre-2000s era) may carry ball-lock couplings — verify the face type.</li>",
       service="For Komatsu machines, the model series and build year matter: coupling profile changed from ball-lock to flat-face across the range. Provide model + serial + photo for an accurate match.",
       faqs=[['Do Komatsu excavators use flat-face?', 'Modern Komatsu excavator auxiliary lines use flat-face (ISO 16028 style) couplings.'],
             ['What threads do Komatsu machines use?', 'It varies by market: metric threads are common on machines for Asia and Europe, while North American machines often use ORFS or NPT. Verify per machine.'],
             ['Are Komatsu couplings standard?', 'Yes — Komatsu uses industry-standard profiles, so aftermarket flat-face or ISO 7241 couplings can be sourced.']]),
  dict(brand='Hitachi', slug='hitachi',
       intro="Hitachi Construction Machinery builds excavators, wheel loaders and compact equipment. Modern Hitachi excavator auxiliary lines use flat-face (ISO 16028 style) couplings; older machines may use ISO 7241 ball-lock. Compact excavators follow the same pattern at smaller sizes.",
       fam1='Excavator auxiliaries', std1='Flat-face (ISO 16028 style)', size1='1/2&quot; - 3/4&quot;', thr1='ORFS / metric',
       fam2='Compact excavator lines', std2='Flat-face (ISO 16028 style)', size2='3/8&quot; - 1/2&quot;', thr2='ORFS / NPT',
       fam3='Older machines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Hitachi excavator auxiliaries are flat-face on modern machines — match the profile on replacement couplings.</li><li>Compact Hitachi machines use smaller flat-face sizes (3/8&quot; - 1/2&quot;).</li><li>Verify thread ends per market before ordering.</li>",
       service="Provide the Hitachi model series and the coupling face type. Hitachi auxiliary hose kits vary by model year; a photo of the existing half is the fastest way to confirm.",
       faqs=[['Do Hitachi excavators use flat-face?', 'Modern Hitachi excavator auxiliary lines use flat-face (ISO 16028 style) couplings.'],
             ['What size couplings on compact Hitachi machines?', 'Compact Hitachi excavators typically use 3/8&quot; to 1/2&quot; flat-face couplings on auxiliary lines.'],
             ['Are Hitachi and Komatsu couplings the same?', 'Both use industry-standard flat-face and ISO 7241 profiles, but part numbers differ — match by profile, not by brand.']]),
  dict(brand='Volvo CE', slug='volvo-ce',
       intro="Volvo Construction Equipment builds excavators, wheel loaders, articulated haulers and compact machines. Volvo CE auxiliary lines use flat-face (ISO 16028 style) couplings on modern machines; older models and certain attachments may carry ISO 7241 ball-lock couplings.",
       fam1='Excavator auxiliaries', std1='Flat-face (ISO 16028 style)', size1='1/2&quot; - 3/4&quot;', thr1='ORFS / metric',
       fam2='Wheel loader auxiliaries', std2='Flat-face (ISO 16028 style)', size2='1/2&quot; - 3/4&quot;', thr2='ORFS / NPT',
       fam3='Older machines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot; - 3/4&quot;', thr3='NPT / BSPP',
       bullets="<li>Volvo CE machines use flat-face couplings on modern auxiliary circuits — the default for low-spill attachment changeover.</li><li>European-built Volvo machines commonly use metric or ORFS threads; verify per machine.</li><li>High-flow circuits require larger flat-face sizes rated for the flow.</li>",
       service="Volvo CE machines are specified per market; include the model, build year and a photo of the coupling halves when ordering replacements.",
       faqs=[['Do Volvo CE excavators use flat-face?', 'Modern Volvo CE excavator auxiliary lines use flat-face (ISO 16028 style) couplings.'],
             ['What threads on Volvo machines?', 'European-built Volvo machines often use metric or ORFS; North American machines may use NPT or ORFS. Verify per machine.'],
             ['Can I upgrade an older Volvo machine to flat-face?', 'Yes — replace both halves as a matched set. It reduces spill and contamination during attachment changes.']]),
  dict(brand='Yanmar', slug='yanmar',
       intro="Yanmar builds compact tractors, mini excavators, skid steers and utility equipment. Yanmar compact tractors use ISO 5675 on rear outlets; mini excavators use flat-face (ISO 16028 style) on auxiliary lines; some models carry ball-lock ISO 7241 couplings on service lines.",
       fam1='Compact tractor outlets', std1='ISO 5675 (agricultural)', size1='1/2&quot; ISO 5675', thr1='BSPP / NPT',
       fam2='Mini excavator auxiliaries', std2='Flat-face (ISO 16028 style)', size2='3/8&quot; - 1/2&quot;', thr2='NPT / BSPP',
       fam3='Service lines', std3='Ball-lock ISO 7241 where fitted', size3='1/2&quot;', thr3='NPT / BSPP',
       bullets="<li>Yanmar compact tractor rear outlets are ISO 5675 — the agricultural profile.</li><li>Yanmar mini excavators use flat-face on auxiliary lines at compact sizes.</li><li>Yanmar machines sold in Asia often carry BSPP threads; North American units NPT.</li>",
       service="Yanmar machines are sold worldwide with different thread conventions. Confirm the market with the model — a Yanmar tractor in Asia (BSPP) differs from the same model in North America (often NPT).",
       faqs=[['Do Yanmar tractors use ISO 5675?', 'Yes — Yanmar compact tractor rear outlets use ISO 5675 agricultural couplings.'],
             ['What couplings on Yanmar mini excavators?', 'Yanmar mini excavators use flat-face (ISO 16028 style) couplings on auxiliary lines, typically 3/8&quot; to 1/2&quot;.'],
             ['Are Yanmar couplings standard?', 'Yes — Yanmar uses industry-standard profiles, so standard couplings are available aftermarket.']]),
  dict(brand='Massey Ferguson', slug='massey-ferguson',
       intro="Massey Ferguson (AGCO) builds tractors and combines used worldwide. MF tractor rear SCV outlets use ISO 5675 couplings; some models and markets may also carry ISO 7241 ball-lock couplings on auxiliary circuits.",
       fam1='Tractor rear outlets', std1='ISO 5675 (agricultural)', size1='1/2&quot; ISO 5675', thr1='BSPP / NPT',
       fam2='Auxiliary / loader lines', std2='Ball-lock ISO 7241 or flat-face', size2='1/2&quot; - 3/4&quot;', thr2='BSPP / NPT',
       fam3='Service lines', std3='Ball-lock ISO 7241', size3='1/2&quot; - 3/4&quot;', thr3='BSPP / NPT',
       bullets="<li>MF tractor rear outlets are ISO 5675 — match with agricultural couplings and seals.</li><li>Loader and auxiliary circuits may use ISO 7241 ball-lock or flat-face depending on configuration.</li><li>European MF tractors typically use BSPP threads; export units vary.</li>",
       service="For MF tractors, confirm the outlet profile (ISO 5675 rear outlets vs ISO 7241 auxiliary lines) and the thread per market. The model number plus a coupling photo settles it.",
       faqs=[['Do Massey Ferguson tractors use ISO 5675?', 'Yes — MF tractor rear SCV outlets use ISO 5675 agricultural couplings.'],
             ['What are the loader lines on MF tractors?', 'MF loader circuits commonly use ISO 7241 ball-lock couplings, and newer models may use flat-face. Check the face type.'],
             ['Are MF and Fendt couplings the same?', 'Both AGCO brands follow industry standards (ISO 5675 / ISO 7241 / ISO 16028), so profiles match — but confirm per machine model.']]),
]

pages = []
for b in BRANDS:
    bullets_html = b['bullets']
    faq_rows = ''.join('<h3>%s</h3><p>%s</p>' % (esc(q), esc(a)) for q, a in b['faqs'])
    content = TPL.format(
        brand=esc(b['brand']), slug=b['slug'],
        lines=j([b['fam1'], b['std1'], b['size1'], b['thr1']]),
        faqs=j(b['faqs']),
        intro=b['intro'], fam1=b['fam1'], std1=b['std1'], size1=b['size1'], thr1=b['thr1'],
        fam2=b['fam2'], std2=b['std2'], size2=b['size2'], thr2=b['thr2'],
        fam3=b['fam3'], std3=b['std3'], size3=b['size3'], thr3=b['thr3'],
        bullets=bullets_html, service=b['service'], faqhtml=faq_rows,
    )
    path = os.path.join(BASE, b['slug'] + '-hydraulic-quick-couplers.astro')
    open(path, 'w', encoding='utf-8').write(content)
    pages.append(path)
print('S2 品牌页生成:', len(pages), '页')
for p in pages: print(' OK', os.path.basename(p))
