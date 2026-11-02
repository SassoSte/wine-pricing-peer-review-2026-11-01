from pathlib import Path
import json
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.comments import Comment
P=Path(__file__).resolve().parent;r=json.loads((P/'consistent-price-validation-v2.json').read_text());c=json.loads((P/'consistent-price-config-v2.json').read_text());wb=Workbook();s=wb.active;s.title='Read me'
for row in [['Consistent pricing layer v2','Expert-guided low-end calibration; not market validation'],['What changed','Two Northeast knots added: amber35/120 near450USD; brown40/130 at300USDceiling. Existingcalibration andanchors unchanged.'],['Upper-bound treatment','300is used as the ceiling-active endpoint, consistent with near300guidance. It isnot a verifiedcostfloor or exacttransactionprice.'],['Scope','Wholefilledcask,comparable seat/reference-status,samevolume,mint,initialrelease/distributorterms. Fees/taxes/deliveryexcluded.'],['Regional transfer','Low-endshape is calibrated fromNortheast only. Otherregions inheritsharedproportionaldiscounts; sixregionalanchors are modelinferred.'],['Support','Fullattribute-lossrange now covered byknots, but unobservedcombinations andotherregions are not independentlyvalidated. No priceconfidenceinterval supplied.'],['Controls','1250positiveprices,3000monotonicsteps,3750referencechecks; old230in-spanprices and10accepted-fitestimates unchanged.'],['Edit policy','Bluecells are frozen config/sourcevalues; formulasareblack/green. Attribute-losscolumns areexternalmodeloutputs; editing attributenames doesnotrerunmodel.']]:s.append(row)
curve=wb.create_sheet('Curve');curve.append(['Attribute loss','Log discount'])
for row in c['log_discount_knots']:curve.append(row)
last=curve.max_row
anchors=wb.create_sheet('Anchors');anchors.append(['Region','Reference USD','Source']);idx={}
for i,(z,a) in enumerate(c['regional_anchors'].items(),2):idx[z]=i;anchors.append([z,a['price'],a['status']])
grid=wb.create_sheet('Prices');grid.append(['Region','Shade','Vintage years','Tare lb','Attribute loss','Reference USD','Log discount','New price USD','Prior price USD','Change USD','Calibration status','Regional low-end transfer assumed']);lookup={}
for i,q in enumerate(r['grid'],2):
 z,shade,age,tare=q['offering'];lookup[tuple(q['offering'])]=i
 def segment(lo,hi):return f'Curve!B{lo}+(E{i}-Curve!A{lo})*(Curve!B{hi}-Curve!B{lo})/(Curve!A{hi}-Curve!A{lo})'
 form=segment(last-1,last)
 for hi in range(last-1,2,-1):form=f'IF(E{i}<=Curve!A{hi},{segment(hi-1,hi)},{form})'
 grid.append([z,shade,age,tare,q['attribute_loss'],f'=Anchors!B{idx[z]}','='+form,f'=F{i}*EXP(-G{i})',q['previous_price_usd'],f'=H{i}-I{i}',q['calibration_status'],q['regional_low_end_transfer_assumed']]);grid.cell(i,5).comment=Comment('Frozen base-attribute loss from consistent-price-validation-v2.json.','Source')
checks=wb.create_sheet('Checks');checks.append(['Case','Accepted/constraint USD','New USD','Prior model USD','New minus prior USD','Interpretation']);old=json.loads((P/'consistent-price-validation-v1.json').read_text())['fit_observations'];priorby={q['id']:q for q in old}
for i,q in enumerate(r['prior_accepted_checks'],2):
 ref=lookup[tuple(priorby[q['id']]['offering'])];checks.append([q['id'],q['accepted_price'],f'=Prices!H{ref}',q['prior_model_price'],f'=C{i}-D{i}','Post-disclosure acceptance used in originalcalibration; existingfit unchanged'])
for q in r['constraints']:
 i=checks.max_row+1;ref=lookup[tuple(q['offering'])];oldrow=next(v for v in r['grid'] if v['offering']==q['offering']);checks.append([q['id'],q['target'],f'=Prices!H{ref}',oldrow['previous_price_usd'],f'=C{i}-D{i}',q['type']])
summary=wb.create_sheet('Region bounds');summary.append(['Region','Minimum USD','Maximum USD','Anchor source','Caution'])
for i,(z,a) in enumerate(c['regional_anchors'].items(),2):
 start=2+(i-2)*125;end=start+124;summary.append([z,f'=MIN(Prices!H{start}:H{end})',f'=MAX(Prices!H{start}:H{end})',a['status'],'Sharedcurve transfer outsideNE; modeledbounds,notmarket confidenceinterval'])
for sh in wb:
 sh.freeze_panes='A2';sh.auto_filter.ref=sh.dimensions;sh.sheet_view.showGridLines=False;sh.row_dimensions[1].height=30
 for row in sh:
  for cell in row:cell.font=Font(name='Arial',size=10,color='008000' if cell.data_type=='f' and '!' in cell.value else '000000' if cell.data_type=='f' else '1F2937');cell.alignment=Alignment(vertical='top')
 for cell in sh[1]:cell.font=Font(name='Arial',size=10,bold=True,color='FFFFFF');cell.fill=PatternFill('solid',fgColor='243746');cell.alignment=Alignment(wrap_text=True)
 for col in sh.columns:sh.column_dimensions[col[0].column_letter].width=25
for sh in [curve,anchors]:
 for row in sh.iter_rows(min_row=2):
  for cell in row:
   if isinstance(cell.value,(float,int)):cell.font=Font(name='Arial',color='0000FF');cell.fill=PatternFill('solid',fgColor='FFF2CC')
for sh,cols in [(anchors,[2]),(grid,[6,8,9,10]),(checks,[2,3,4,5]),(summary,[2,3])]:
 for row in range(2,sh.max_row+1):
  for col in cols:sh.cell(row,col).number_format='"$"#,##0.00;[Red]("$"#,##0.00)'
s.column_dimensions['A'].width=25;s.column_dimensions['B'].width=110
for row in range(2,s.max_row+1):s.cell(row,2).alignment=Alignment(wrap_text=True);s.row_dimensions[row].height=45
checks.column_dimensions['A'].width=31;checks.column_dimensions['F'].width=70;grid.column_dimensions['K'].width=35;summary.column_dimensions['E'].width=75
wb.save(P/'consistent-prices-v2.xlsx');print('V2workbook written.')
