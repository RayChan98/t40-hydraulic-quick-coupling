# -*- coding: utf-8 -*-
"""T-40 建站：批量生成产品/应用/OEM 页面（ProductPageTemplate 驱动）"""
import os, json

BASE = r'D:\kravzik-work\t40-hydraulic-quick-coupling\site\src\pages'

TPL = '''---
import Layout from '../layouts/Layout.astro';
import ProductPageTemplate from '../components/ProductPageTemplate.astro';
const specs = {specs};
const features = {features};
const applications = {apps};
const faqs = {faqs};
const trust = {trust};
---
<Layout title="{title}" description="{desc}">
  <ProductPageTemplate
    model="{model}"
    series="{series}"
    category="{cat}"
    tagline="{tagline}"
    description="{description}"
    specs={{specs}}
    features={{features}}
    applications={{applications}}
    faqs={{faqs}}
    trustPoints={{trust}}
  >
    <Fragment slot="chapters">
      {chapters}
    </Fragment>
  </ProductPageTemplate>
</Layout>
'''

def j(o):
    return json.dumps(o, ensure_ascii=False)

def esc(s):
    """JSX 双引号属性转义"""
    return s.replace('"', '&quot;')

pages = [
  dict(file='agricultural-hydraulic-couplings.astro',
    model='Agricultural Hydraulic Couplings', series='ISO 5675', cat='Tractor Quick Couplings',
    tagline='Free-flow tractor-to-implement couplings built for dusty fields, long duty cycles and one-handed hookup.',
    description='ISO 5675 agricultural couplings are the standard quick coupling for tractor implements and farm machinery. The free-flow poppet design supports high return flow, and the robust ball-lock sleeve stands up to dust, vibration and repeated connect cycles. Available for ISO 5675 implements with NPT or BSPP ends in the common 1/2" size, plus matching dust caps.',
    specs=[['Standard','ISO 5675 (agricultural hydraulic quick couplings)'],['Size','1/2" (DN 12.5) dominant; other sizes on request'],['Working pressure','Typically 200 bar (3,000 psi) class'],['Materials','Carbon steel, zinc or nickel plated; stainless option'],['Connections','NPT, BSPP male/female per implement standard'],['Flow','Free-flow poppet design for high return flow'],['Temperature','-20 C to +100 C typical'],['Applications','Tractors, implements, balers, sprayers, loaders']],
    features=['Free-flow poppet for high return flow','Dust-resistant sleeve and ball lock','One-handed connect/disconnect','Interchangeable per ISO 5675 with major ranges','Caps and plugs available per size','Steel or stainless body'],
    apps=['Tractors','Implements','Balers','Sprayers','Front loaders','Hay equipment'],
    faqs=[{'q':'Is 1/2" ISO 5675 the universal tractor size?','a':'For most implements yes - 1/2" ISO 5675 dominates agricultural quick couplings. Larger flow implements may use flat-face ISO 16028. Check the implement hose ends before ordering.'},{'q':'What threads do tractor couplings use?','a':'Most ISO 5675 couplings come with NPT or BSPP threads; older European machines often use BSPP. Specify the thread of the implement hose.'}],
    trust=['ISO 5675 dimensional interchange','Caps & plugs stocked','Custom thread options','24h quote response'],
    title='Agricultural Hydraulic Couplings (ISO 5675) - Tractor Implements | Hydraulic Quick Couplings',
    desc='ISO 5675 agricultural hydraulic quick couplings for tractors and implements. Free-flow poppet, ball-lock sleeve, 1/2" with NPT/BSPP. Dust caps available.',
    chapters='<section class="bg-white"><div class="mx-auto max-w-7xl px-4 py-16 sm:px-6"><h2 class="text-2xl font-extrabold text-navy-950">What Makes a Good Tractor Coupling</h2><p class="mt-4 max-w-3xl text-sm leading-relaxed text-slate-600">Field work is brutal on couplings: dust, mud, vibration and hundreds of connect cycles per season. ISO 5675 couplings survive because the free-flow poppet keeps return flow high and the sleeve keeps debris out of the locking mechanism. The most common failure is seal wear from contamination - fitting dust caps when implements are parked is the single best maintenance habit.</p></div></section>'),
  dict(file='ball-lock-hydraulic-couplings.astro',
    model='Ball Lock Hydraulic Couplings', series='Ball-Lock Series', cat='Quick-Disconnect Couplings',
    tagline='The classic sleeve-operated ball-lock design - fast, dependable and rebuildable with seal kits.',
    description='Ball lock hydraulic couplings use hardened balls retained in a sleeve to lock the plug in the coupler. Pull the sleeve back, insert, release - connected. They are the most widely used quick-disconnect design in industry because they are fast, compact and cheap to rebuild. We supply ball-lock couplings in ISO 7241 Series A/B, agricultural and custom profiles.',
    specs=[['Design','Sleeve-operated hardened ball lock'],['Sizes','1/4" to 1" common; larger on request'],['Pressure','200-250 bar class (size and material dependent)'],['Materials','Carbon steel plated, stainless, brass'],['Seals','NBR standard; FKM/HNBR for high temp or bio-oils'],['Rebuild','O-ring and complete seal kits available'],['Threads','NPT, BSPP, BSPT, JIC, ORFS'],['Applications','Industrial, mobile, agricultural hydraulics']],
    features=['One-handed sleeve connection','Hardened balls for long cycle life','Rebuildable - seal kits stocked','Wide thread and material choice','Compact envelope','Consistent low pressure drop'],
    apps=['Machine tools','Hydraulic power units','Test benches','Mobile equipment','Agricultural implements'],
    faqs=[{'q':'When do ball-lock couplings fail?','a':'Three common causes: contamination in the sleeve/ball area, worn O-rings (internal weep), and connecting under residual pressure which forces the sleeve and damages the locking groove.'},{'q':'Can I rebuild instead of replace?','a':'Usually yes. Replace the O-rings and, if scored, the ball set. Keep the seal kit number with the coupling.'}],
    trust=['Rebuildable with stocked seal kits','Hardened ball construction','Custom threads & materials','24h quote response'],
    title='Ball Lock Hydraulic Couplings - Sleeve Quick Disconnect | Hydraulic Quick Couplings',
    desc='Ball lock hydraulic quick couplings: sleeve-operated hardened ball lock, ISO 7241 profiles, 1/4"-1", NPT/BSPP/JIC/ORFS. Rebuildable with seal kits.',
    chapters='<section class="bg-white"><div class="mx-auto max-w-7xl px-4 py-16 sm:px-6"><h2 class="text-2xl font-extrabold text-navy-950">Keep Ball Lock Couplings Alive</h2><p class="mt-4 max-w-3xl text-sm leading-relaxed text-slate-600">Cap disconnected halves, wipe the nose and socket before each connection, and never force a connection under residual pressure. With those three habits, a ball-lock coupling outlives most machines. When it finally weeps, a seal kit restores it for a fraction of replacement cost.</p></div></section>'),
  dict(file='pin-lock-hydraulic-couplings.astro',
    model='Pin Lock Hydraulic Couplings', series='Pin-Lock Series', cat='Positive-Lock Couplings',
    tagline='Positive locking pins for high-vibration circuits and applications where a sleeve could be accidentally pulled.',
    description='Pin lock hydraulic couplings replace the ball/sleeve mechanism with positive locking pins. The design resists accidental disconnection under vibration and shock loads, making it a safety-preferred choice for heavy mobile equipment and high-flow circuits. Sleeve release still allows one-handed operation.',
    specs=[['Design','Positive pin-lock mechanism'],['Sizes','1/4" to 1" common'],['Pressure','200-350 bar class (size and material dependent)'],['Materials','Carbon steel plated; stainless option'],['Locking','Positive pins, sleeve-released'],['Threads','NPT, BSPP, JIC, ORFS'],['Applications','Heavy mobile, high-vibration, high-flow'],['Options','Lockable sleeve, dust caps']],
    features=['Positive locking under vibration','No accidental sleeve release','High-flow variants','One-handed operation','Steel or stainless','Custom threads'],
    apps=['Excavators','Mining equipment','Forestry','High-flow mobile circuits','Heavy plant'],
    faqs=[{'q':'Pin lock vs ball lock - when does it matter?','a':'If a machine vibrates hard or an operator can bump the sleeve (forestry, mining), pin lock prevents accidental disconnect. For general industrial duty, ball lock is cheaper and sufficient.'}],
    trust=['Positive-lock safety design','High-flow variants','Custom threads & materials','24h quote response'],
    title='Pin Lock Hydraulic Couplings - Positive Lock for Heavy Duty | Hydraulic Quick Couplings',
    desc='Pin lock hydraulic couplings: positive locking pins resist accidental disconnect under vibration. For excavators, mining, forestry. NPT/BSPP/JIC/ORFS.',
    chapters='<section class="bg-white"><div class="mx-auto max-w-7xl px-4 py-16 sm:px-6"><h2 class="text-2xl font-extrabold text-navy-950">Where Pin Lock Earns Its Keep</h2><p class="mt-4 max-w-3xl text-sm leading-relaxed text-slate-600">Any circuit that disconnects itself under vibration is a pin-lock candidate: forestry grapples, mining hammers, demolition tools. If you have ever replaced a coupling after a sleeve was knocked open, pin lock is the upgrade.</p></div></section>'),
  dict(file='1-2-inch-hydraulic-quick-couplers.astro',
    model='1/2" Hydraulic Quick Couplers', series='1/2" (DN 12.5)', cat='Size Guide',
    tagline='The most common mobile-equipment size - Series A, Series B, flat-face and agricultural profiles with every thread option.',
    description='1/2" hydraulic quick couplers are the default size for mobile equipment auxiliary circuits: skid steer attachments, tractor implements, excavator thumb circuits and industrial hose reels. This page is your 1/2" spec reference - profiles, threads, pressure classes and the questions to answer before ordering.',
    specs=[['Nominal size','1/2" (DN 12.5)'],['Profiles','ISO 7241 Series A / Series B, ISO 16028 flat face, ISO 5675 agricultural'],['Threads','NPT 1/2", BSPP 1/2", JIC 3/4"-16, ORFS 3/4"-16, BSPT'],['Pressure','200-350 bar depending on profile and material'],['Materials','Carbon steel, stainless, brass'],['Typical use','Skid steers, tractors, excavator aux lines, hose reels'],['Flow','Match to circuit: check pressure-drop curves for continuous duty'],['Accessories','Dust caps, plugs, protective covers']],
    features=['Covers every 1/2" profile','NPT/BSPP/JIC/ORFS thread options','Steel, stainless or brass','Caps and plugs stocked','Custom assemblies on request'],
    apps=['Skid steer attachments','Tractor implements','Excavator aux circuits','Hose reels','Test equipment'],
    faqs=[{'q':'1/2" NPT or 1/2" BSPP - which thread?','a':'NPT is US standard, BSPP is the parallel pipe thread common in Europe/Asia. They are not compatible - a BSPP male will not seal in an NPT female. Match the hose fitting exactly.'},{'q':'What pressure can a 1/2" coupler handle?','a':'Typically 200-350 bar depending on profile (flat-face tends higher) and material. Confirm the data sheet for the exact model.'}],
    trust=['All 1/2" profiles in one place','Threads NPT/BSPP/JIC/ORFS','Caps & plugs stocked','24h quote response'],
    title='1/2" Hydraulic Quick Couplers - Profiles, Threads & Specs | Hydraulic Quick Couplings',
    desc='1/2" hydraulic quick couplers: ISO 7241 A/B, ISO 16028 flat face, ISO 5675 agricultural. NPT/BSPP/JIC/ORFS threads, steel/stainless/brass, caps & plugs.',
    chapters='<section class="bg-white"><div class="mx-auto max-w-7xl px-4 py-16 sm:px-6"><h2 class="text-2xl font-extrabold text-navy-950">Four Questions Before You Order 1/2" Couplers</h2><ol class="mt-6 space-y-3"><li class="text-sm text-slate-700">1. Profile - Series A, Series B, flat face or agricultural? Match the machine and the existing halves.</li><li class="text-sm text-slate-700">2. Thread - NPT, BSPP, JIC or ORFS on each end? Not interchangeable.</li><li class="text-sm text-slate-700">3. Material - steel for general duty, stainless for washdown/corrosive media.</li><li class="text-sm text-slate-700">4. Quantity & caps - fleet refits save when ordered as sets with caps.</li></ol></div></section>'),
  dict(file='hydraulic-quick-couplings-for-agriculture.astro',
    model='Hydraulic Quick Couplings for Agriculture', series='Application', cat='Applications',
    tagline='Tractors, implements and self-propelled machines run on quick couplings - here is how to spec and maintain them in the field.',
    description='Agriculture is the biggest single market for hydraulic quick couplings. This page covers the coupling types used on farm machinery, the standards that apply, and the maintenance habits that keep implements working through the season.',
    specs=[['Main standard','ISO 5675 (tractor implements)'],['Also common','ISO 7241 Series A/B (general), ISO 16028 flat face (high-flow/high-tech implements)'],['Dominant size','1/2" (DN 12.5)'],['Environment','Dust, mud, UV, bio-oils, vibration'],['Common failures','Seal wear, contamination, stuck sleeves'],['Maintenance','Caps on parked implements, wipe before connect, seal kits']],
    features=['ISO 5675 and flat-face coverage','Dust cap recommendations','Bio-oil seal options (FKM/HNBR)','Fleet-order support'],
    apps=['Tractors','Combines','Sprayers','Balers','Self-propelled sprayers','Front loaders'],
    faqs=[{'q':'Why do agricultural couplings fail so often?','a':'Dust and contamination are the killers. A grain or soil particle trapped on a seal face becomes a leak in weeks. Cap every disconnected coupling.'}],
    trust=['Agricultural coupling specialist','Caps & plugs stocked','Bio-oil seal options','24h quote response'],
    title='Hydraulic Quick Couplings for Agriculture - Tractor & Implement Guide | Hydraulic Quick Couplings',
    desc='Agricultural hydraulic quick couplings: ISO 5675 tractor implements, flat-face for high-flow, dust caps, bio-oil seals and field maintenance.',
    chapters='<section class="bg-white"><div class="mx-auto max-w-7xl px-4 py-16 sm:px-6"><h2 class="text-2xl font-extrabold text-navy-950">Field Maintenance That Pays</h2><p class="mt-4 max-w-3xl text-sm leading-relaxed text-slate-600">Fit dust caps on every implement coupling at the end of the season. Wipe the faces before each hookup. Replace seals at the first weep rather than at failure. A cap costs less than a litre of spilled hydraulic oil.</p></div></section>'),
  dict(file='hydraulic-quick-couplings-for-construction.astro',
    model='Hydraulic Quick Couplings for Construction', series='Application', cat='Applications',
    tagline='Excavators, skid steers and loaders switch attachments all day - flat-face CUP couplings keep that safe and spill-free.',
    description='Construction equipment changes attachments constantly, which is exactly what quick couplings are for. On these machines, flat-face ISO 16028 couplings dominate because operators connect under residual pressure and sites demand minimal spill. This page covers the standard choices for construction duty and the safety rules that apply.',
    specs=[['Main standard','ISO 16028 flat face (mobile equipment)'],['Also common','ISO 7241 Series A/B on older machines'],['Key feature','Connect-under-pressure (CUP) variants'],['Dominant sizes','1/2" and 3/4"'],['Safety','Never inspect a leak by hand - fluid injection injuries'],['Maintenance','Caps, seal kits, face inspection']],
    features=['Flat-face CUP focus','Excavator & skid steer coverage','Safety-first guidance','Fleet standardization support'],
    apps=['Excavators','Skid steer loaders','Compact loaders','Demolition tools','Snow removal','Material handlers'],
    faqs=[{'q':'Should our fleet standardize on flat-face?','a':'If operators hot-swap attachments (multi-tool skid steers, quick couplers on excavators), flat-face CUP is the safe, spill-free standard. Retrofit kits keep the change affordable.'}],
    trust=['Flat-face CUP specialist','Fleet retrofit support','Safety guidance','24h quote response'],
    title='Hydraulic Quick Couplings for Construction - Flat Face & CUP | Hydraulic Quick Couplings',
    desc='Construction hydraulic quick couplings: ISO 16028 flat-face with connect-under-pressure for excavators and skid steers. Safety and spill-free switching.',
    chapters='<section class="bg-white"><div class="mx-auto max-w-7xl px-4 py-16 sm:px-6"><h2 class="text-2xl font-extrabold text-navy-950">The One Safety Rule</h2><p class="mt-4 max-w-3xl text-sm leading-relaxed text-slate-600">Never check a suspected high-pressure leak with your hand. Fluid injection injuries are medical emergencies. Use a piece of cardboard, depressurize the circuit, and replace the weeping coupling.</p></div></section>'),
  dict(file='hydraulic-quick-couplings-for-industrial.astro',
    model='Hydraulic Quick Couplings for Industrial', series='Application', cat='Applications',
    tagline='Machine tools, presses and process lines run on ISO 7241 - dependable, rebuildable, and spec-able to your exact thread.',
    description='Industrial hydraulics are the home of ISO 7241-1 Series A couplings: machine tools, presses, power units, test benches and process lines. This page is the industrial buyer quick reference - what to specify, how to standardize across a plant, and how to keep coupling inventory low.',
    specs=[['Main standard','ISO 7241-1 Series A (and B where European OEM specifies)'],['Dominant sizes','1/4" to 3/4"'],['Threads','NPT, BSPP, JIC, ORFS - machine-dependent'],['Environment','Indoor, clean; media varies (HLP, HFD-R, water-glycol)'],['Key advantage','Rebuildable, low cost, universal availability'],['Inventory tip','Standardize on one profile + one thread per plant']],
    features=['Series A/B industrial focus','Plant standardization advice','Media compatibility guidance','Seal kit support'],
    apps=['Machine tools','Presses','Power units','Test benches','Die casting','Process lines'],
    faqs=[{'q':'How do we cut coupling inventory?','a':'Standardize each machine type on a single profile and thread combination. With ISO 7241 Series A + one thread per pressure class, one shelf of couplings and seal kits serves most of a plant.'}],
    trust=['Industrial standardization help','Seal kits stocked','Media compatibility guidance','24h quote response'],
    title='Hydraulic Quick Couplings for Industrial - ISO 7241 Plant Guide | Hydraulic Quick Couplings',
    desc='Industrial hydraulic quick couplings: ISO 7241-1 Series A/B for machine tools, presses, power units. Thread standards, media compatibility, plant standardization.',
    chapters='<section class="bg-white"><div class="mx-auto max-w-7xl px-4 py-16 sm:px-6"><h2 class="text-2xl font-extrabold text-navy-950">Standardize, Then Stock</h2><p class="mt-4 max-w-3xl text-sm leading-relaxed text-slate-600">Plants that standardize on one profile and one thread per pressure class cut coupling inventory 40-60%. Maintenance stops guessing, procurement buys volume, and rebuilds become a shelf item.</p></div></section>'),
  dict(file='oem-supply.astro',
    model='OEM & Custom Coupling Supply', series='B2B Supply', cat='Volume & Custom',
    tagline='Tell us the standard, size, thread, quantity and finish - we handle the supply, packaging and documentation.',
    description='We support OEMs, distributors and fleet owners with volume supply of hydraulic quick couplings: standard ISO 7241/16028/5675 ranges, custom threads and materials, private packaging, and the documentation importers need. No rigid MOQ games - tell us what you need and we quote the honest path.',
    specs=[['What we supply','ISO 7241 A/B, ISO 16028, ISO 5675 quick couplings; seal kits; caps & plugs'],['Custom options','Threads, materials (steel/stainless/brass), plating, sleeve colors, private packaging'],['Documentation','Packing lists, COO, test reports on request'],['Lead time','Standard sizes stocked; custom specs quoted per order'],['MOQ','Flexible - quoted per line item'],['Payment','T/T, L/C; terms discussed per order']],
    features=['All ISO quick-coupling ranges','Custom threads & materials','Private packaging option','Documentation for importers','Flexible MOQ & lead times'],
    apps=['OEM hydraulic builders','Distributors','Fleet owners','Importers','Maintenance contractors'],
    faqs=[{'q':'Can you match our existing part numbers?','a':'Yes - send us your part number or a sample; we cross-reference to the ISO profile and quote the matching range with full dimensions for your approval.'},{'q':'What is your typical lead time?','a':'Standard sizes from stock; custom specs typically 2-4 weeks depending on quantity and finish. Quote confirms.'}],
    trust=['All ISO ranges in one quote','Custom specs welcome','Documentation ready','24h response'],
    title='OEM & Custom Hydraulic Coupling Supply - Volume, Custom Specs | Hydraulic Quick Couplings',
    desc='OEM and volume supply of hydraulic quick couplings: ISO 7241/16028/5675, custom threads and materials, private packaging, importer documentation.',
    chapters='<section class="bg-white"><div class="mx-auto max-w-7xl px-4 py-16 sm:px-6"><h2 class="text-2xl font-extrabold text-navy-950">How We Quote</h2><ol class="mt-6 space-y-3"><li class="text-sm text-slate-700">1. You send: standard/size/thread/quantity (or part number/sample).</li><li class="text-sm text-slate-700">2. We confirm: profile match, dimensions, lead time, price.</li><li class="text-sm text-slate-700">3. We deliver: packed, documented, on schedule.</li></ol></div></section>'),
]

for p in pages:
    content = TPL.format(
        specs=j(p['specs']), features=j(p['features']), apps=j(p['apps']), faqs=j(p['faqs']),
        title=esc(p['title']), desc=esc(p['desc']), model=esc(p['model']), series=esc(p['series']), cat=esc(p['cat']),
        tagline=esc(p['tagline']), description=esc(p['description']), trust=j(p['trust']), chapters=p['chapters'],
    )
    path = os.path.join(BASE, p['file'])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK', p['file'])
print('TOTAL', len(pages))
