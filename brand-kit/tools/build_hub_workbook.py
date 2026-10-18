#!/usr/bin/env python3
"""Build the polished, offline Excel view from Brand Kit source-of-truth JSON."""
from __future__ import annotations
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "ahangban-brand-intelligence-hub.xlsx"
BLUE = "185ADB"
DARK_BLUE = "1248B2"
INK = "111111"
CHARCOAL = "222222"
PALE = "EAF1FF"
PAPER = "F4F4F4"
WHITE = "FFFFFF"
MUTED = "666666"
LINE = "E5E5E5"
STATUS_COLORS = {
    "VERIFIED": "D9EAD3", "COMPLETE": "D9EAD3", "INCOMPLETE": "FCE4D6",
    "NEEDS_REVIEW": "FFF2CC", "UNKNOWN": "E7E6E6", "UNVERIFIED": "FCE4D6",
    "ACTIVE": "D9EAD3", "PLANNED": "DDEBF7", "INACTIVE": "E7E6E6",
}


def read(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def style_title(ws, title: str, subtitle: str, last_col: int):
    end = get_column_letter(last_col)
    ws.merge_cells(f"A1:{end}1")
    ws["A1"] = title
    ws["A1"].fill = PatternFill("solid", fgColor=INK)
    ws["A1"].font = Font(name="Aptos Display", size=19, bold=True, color=WHITE)
    ws["A1"].alignment = Alignment(horizontal="right", vertical="center")
    ws.row_dimensions[1].height = 38
    ws.merge_cells(f"A2:{end}2")
    ws["A2"] = subtitle
    ws["A2"].fill = PatternFill("solid", fgColor=PALE)
    ws["A2"].font = Font(name="Aptos", size=10, color=CHARCOAL)
    ws["A2"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    ws.row_dimensions[2].height = 34
    ws.sheet_view.rightToLeft = True
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_margins.left = 0.25
    ws.page_margins.right = 0.25
    ws.page_margins.top = 0.45
    ws.page_margins.bottom = 0.45
    ws.oddFooter.center.text = "آهنگ‌بان · Brand Intelligence Hub · &[Page] / &[Pages]"


def style_header(ws, row: int, start_col: int, end_col: int):
    for col in range(start_col, end_col + 1):
        c = ws.cell(row, col)
        c.fill = PatternFill("solid", fgColor=BLUE)
        c.font = Font(name="Aptos", bold=True, color=WHITE, size=10)
        c.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
        c.border = Border(bottom=Side(style="medium", color=DARK_BLUE))
    ws.row_dimensions[row].height = 35


def style_data(ws, min_row: int, max_row: int, max_col: int):
    for row in ws.iter_rows(min_row=min_row, max_row=max_row, max_col=max_col):
        for cell in row:
            cell.font = Font(name="Aptos", size=10, color=INK)
            cell.alignment = Alignment(horizontal="right", vertical="top", wrap_text=True)
            cell.border = Border(bottom=Side(style="hair", color=LINE))
            if cell.row % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F8FAFE")


def add_table(ws, name: str, header_row: int, last_row: int, last_col: int):
    if last_row <= header_row:
        ws.auto_filter.ref = f"A{header_row}:{get_column_letter(last_col)}{header_row}"
        return
    table = Table(displayName=name, ref=f"A{header_row}:{get_column_letter(last_col)}{last_row}")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    ws.add_table(table)


def status_format(ws, col: int, first_row: int, last_row: int):
    letter = get_column_letter(col)
    for value, color in STATUS_COLORS.items():
        ws.conditional_formatting.add(f"{letter}{first_row}:{letter}{last_row}", FormulaRule(formula=[f'{letter}{first_row}="{value}"'], fill=PatternFill("solid", fgColor=color)))


def main():
    artists = read("artists/artists.json")["records"]
    assets = read("visual-identity/assets.json")["records"]
    social = read("social-media/accounts.json")["records"]
    music = read("music-catalog/catalog.json")["records"]
    brand = read("brand/identity.json")
    wb = Workbook()
    ws = wb.active
    ws.title = "نمای کلی"
    ws.sheet_properties.tabColor = BLUE
    style_title(ws, "مرکز دانش آهنگ‌بان", "گزارش دیداری از داده‌های واقعیِ موجود در Brand Kit · خروجی از JSONهای منبع حقیقت · بدون اتصال به پایگاه داده سایت", 8)
    widths = [20, 17, 20, 17, 20, 17, 20, 17]
    for i, width in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = width

    cards = [
        (1, 2, "نامزدهای تحقیق هنرمند", f"=COUNTA('هنرمندان'!A5:A{4+len(artists)})", "فهرست سایت نیست"),
        (3, 4, "آثار واقعی در رجیستری", '=COUNTIF(\'کاتالوگ موسیقی\'!A5:A1000,"AB-MUSIC-*")', "نمونه‌های workbook شمرده نشده‌اند"),
        (5, 6, "فایل‌های بصری فهرست‌شده", f"=COUNTA('دارایی‌های بصری'!A5:A{4+len(assets)})", "تأیید/مجوز را ثابت نمی‌کند"),
        (7, 8, "حساب اجتماعی تأییدشده", f'=COUNTIF(\'شبکه‌های اجتماعی\'!F5:F{4+max(1,len(social))},"بله")', "در حال حاضر هیچ‌کدام"),
    ]
    for c1,c2,label,formula,note in cards:
        ws.merge_cells(start_row=4,start_column=c1,end_row=4,end_column=c2)
        ws.merge_cells(start_row=5,start_column=c1,end_row=6,end_column=c2)
        ws.merge_cells(start_row=7,start_column=c1,end_row=7,end_column=c2)
        l=get_column_letter(c1); r=get_column_letter(c2)
        cell=ws.cell(4,c1,label); cell.fill=PatternFill("solid",fgColor=PALE); cell.font=Font(name="Aptos",bold=True,color=DARK_BLUE,size=10); cell.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
        val=ws.cell(5,c1,formula); val.fill=PatternFill("solid",fgColor=WHITE); val.font=Font(name="Aptos Display",bold=True,color=BLUE,size=26); val.alignment=Alignment(horizontal="center",vertical="center")
        nt=ws.cell(7,c1,note); nt.fill=PatternFill("solid",fgColor=WHITE); nt.font=Font(name="Aptos",color=MUTED,size=9); nt.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
        for rr in range(4,8):
            for cc in range(c1,c2+1): ws.cell(rr,cc).border=Border(left=Side(style="thin",color=LINE),right=Side(style="thin",color=LINE),top=Side(style="thin",color=LINE),bottom=Side(style="thin",color=LINE))
    ws.row_dimensions[4].height=29;ws.row_dimensions[5].height=26;ws.row_dimensions[6].height=22;ws.row_dimensions[7].height=28

    def section(row, title):
        ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=8)
        c=ws.cell(row,1,title);c.fill=PatternFill("solid",fgColor=CHARCOAL);c.font=Font(name="Aptos",bold=True,color=WHITE,size=11);c.alignment=Alignment(horizontal="right",vertical="center")
        ws.row_dimensions[row].height=27
    section(9,"محدودیت و خواندن درست اعداد")
    notices=[
        "مخزن شامل کد/دیتابیس سایت نیست؛ تعداد هنرمندان و آثار منتشرشده در سایت قابل تعیین نیست.",
        "۶۵ رکورد هنرمند، نامزدهای صف تحقیق هستند؛ وضعیت صفحه، هویت و اطلاعات حقوقی آن‌ها تأیید نشده است.",
        "حساب‌های اجتماعی از روی فایل طراحی رسمی فرض نمی‌شوند. نام حساب/پیوند در registry عمداً خالی است.",
        "فایل‌های Excel فقط گزارش هستند و منبع اصلی داده نیستند؛ تغییرات را در JSONهای رجیستری اعمال و workbook را دوباره بسازید.",
    ]
    for i,text in enumerate(notices,10):
        ws.merge_cells(start_row=i,start_column=1,end_row=i,end_column=8)
        c=ws.cell(i,1,"• "+text);c.fill=PatternFill("solid",fgColor="FFF8E8" if i==11 else ("F8FAFE" if i%2==0 else WHITE));c.font=Font(name="Aptos",size=10,color=CHARCOAL);c.alignment=Alignment(horizontal="right",vertical="center",wrap_text=True);ws.row_dimensions[i].height=28
    section(15,"شناسه‌های مرجع")
    refs=[("هویت برند","brand/identity.json"),("رجیستری هنرمندان","artists/artists.json"),("آرشیو بصری","visual-identity/assets.json"),("شبکه‌های اجتماعی","social-media/accounts.json"),("کاتالوگ آثار","music-catalog/catalog.json"),("راهنمای کامل","README.md"),("سازندهٔ پرامپت","prompts.html"),("گزارش ممیزی","reports/audit-fa.md")]
    for i,(label,path) in enumerate(refs,16):
        ws.cell(i,1,label).font=Font(name="Aptos",bold=True,color=INK,size=10)
        ws.merge_cells(start_row=i,start_column=2,end_row=i,end_column=8)
        c=ws.cell(i,2,path);c.hyperlink="../"+path;c.style="Hyperlink";c.alignment=Alignment(horizontal="left")
    section(25,"ترکیب صف تحقیق (دادهٔ seed، نه رتبه‌بندی قطعی)")
    for r,priority in enumerate(["P0-Global","P0-RJ","P1","P2"],26):
        ws.cell(r,1,priority);ws.cell(r,2,f'=COUNTIF(\'هنرمندان\'!B5:B{4+len(artists)},A{r})')
        ws.cell(r,1).fill=PatternFill("solid",fgColor=PALE);ws.cell(r,1).font=Font(name="Aptos",bold=True,color=CHARCOAL)
        ws.cell(r,2).font=Font(name="Aptos",bold=True,color=BLUE,size=12)
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.label import DataLabelList
    chart=BarChart();chart.type="bar";chart.style=10;chart.title="نامزدها به تفکیک اولویت";chart.y_axis.title="اولویت seed";chart.x_axis.title="تعداد";chart.height=7.2;chart.width=13.5;chart.legend=None
    chart.add_data(Reference(ws,min_col=2,min_row=26,max_row=29),titles_from_data=False)
    chart.set_categories(Reference(ws,min_col=1,min_row=26,max_row=29));chart.dataLabels=DataLabelList();chart.dataLabels.showVal=True
    ws.add_chart(chart,"D26")
    ws.freeze_panes="A4"

    # Artist archive tracker (one row per source candidate; per-field status remains editable).
    ws=wb.create_sheet("هنرمندان");ws.sheet_properties.tabColor="F0B429"
    headers=["شناسه داخلی","اولویت تحقیق","نام نمایشی فارسی","صورت لاتین از seed","بخش از seed","سبک ثبت‌شده در seed","نامک","وضعیت نام/هویت","نام","نامک","بیوگرافی","تصویر شاخص","منابع معتبر","پیوند رسمی","ارتباط آهنگ/آلبوم","صفحه در سایت","SEO عنوان/توضیح","لینک/تکراری","کنترل نهایی","اقدام بعدی"]
    style_title(ws,"هنرمندان · چک‌لیست تکمیل","نامزدهای صف تحقیق قبلی؛ نه فهرست کامل یا تأییدشدهٔ سایت. شناسه‌های AB-CAND متعلق به Brand Kit هستند، نه سایت.",len(headers))
    for col,h in enumerate(headers,1):ws.cell(4,col,h)
    style_header(ws,4,1,len(headers));ws.freeze_panes="A5"
    for row_num,a in enumerate(artists,5):
        c=a["completion"]
        values=[a["artist_id"],a.get("priority"),a["display_name_fa"],a.get("official_or_latin_name"),a.get("segment_as_reported"),"، ".join(a.get("genres_as_reported",[])),a.get("slug") or "",a.get("identity_status"),c["name"],c["slug"],c["biography"],c["featured_image"],c["reliable_sources"],c["official_links"],c["track_album_relationships"],c["artist_page"],c["seo_title_description"],c["broken_links_and_duplicates"],c["final_quality_control"],a.get("next_action","")]
        for col,val in enumerate(values,1):ws.cell(row_num,col,val)
        ws.row_dimensions[row_num].height=44
    style_data(ws,5,4+len(artists),len(headers));add_table(ws,"ArtistArchive",4,4+len(artists),len(headers))
    widths=[18,16,22,23,18,18,22,19]+[19]*11+[55]
    for i,w in enumerate(widths,1):ws.column_dimensions[get_column_letter(i)].width=w
    for col in range(8,20):status_format(ws,col,5,4+len(artists))
    dv=DataValidation(type="list",formula1='"COMPLETE,INCOMPLETE,NEEDS_REVIEW,VERIFIED,UNKNOWN"',allow_blank=False);ws.add_data_validation(dv);dv.add(f"I5:S{4+len(artists)}")

    # Visual asset inventory.
    ws=wb.create_sheet("دارایی‌های بصری");ws.sheet_properties.tabColor=BLUE
    headers=["مسیر دقیق","نام فایل","دسته","فرمت","کاربرد","ابعاد (عرض×ارتفاع)","نسبت تصویر","حجم (بایت)","وضعیت تصویب","مجوز","آخرین تغییر ثبت‌شده"]
    style_title(ws,"آرشیو دارایی‌های بصری","ابعاد/نسبت در صورت استخراج از فایل. وضعیت مجوز UNKNOWN به معنی مجازبودن نیست.",len(headers))
    for col,h in enumerate(headers,1):ws.cell(4,col,h)
    style_header(ws,4,1,len(headers));ws.freeze_panes="A5"
    for row_num,a in enumerate(assets,5):
        d=a.get("dimensions")
        vals=[a["path"],a["file_name"],a["category"],a["format"],a["purpose"],"×".join(str(v) for v in d) if d else "",a.get("aspect_ratio") or "",a["bytes"],a["approval_status"],a["license_status"],a.get("last_changed_on") or "نامشخص"]
        for col,val in enumerate(vals,1):ws.cell(row_num,col,val)
        ws.cell(row_num,1).hyperlink="../"+a["path"];ws.cell(row_num,1).style="Hyperlink"
        ws.row_dimensions[row_num].height=38
    style_data(ws,5,4+len(assets),len(headers));add_table(ws,"VisualAssets",4,4+len(assets),len(headers))
    for i,w in enumerate([48,34,16,14,60,20,16,16,21,36,22],1):ws.column_dimensions[get_column_letter(i)].width=w
    status_format(ws,9,5,4+len(assets))

    # Social accounts.
    ws=wb.create_sheet("شبکه‌های اجتماعی");ws.sheet_properties.tabColor="5B9BD5"
    headers=["پلتفرم","نام حساب","شناسه","پیوند پروفایل","وضعیت","رسمی تأیید شده؟","دارایی آواتار","بوم/اندازه موجود","بیوگرافی تأییدشده","شاهد/محدودیت","اقدام بعدی"]
    style_title(ws,"شبکه‌های اجتماعی · وضعیت حساب","صرف وجود avatar/template حساب رسمی را ثابت نمی‌کند؛ هیچ handle یا URL ساختگی درج نشده است.",len(headers))
    for col,h in enumerate(headers,1):ws.cell(4,col,h)
    style_header(ws,4,1,len(headers));ws.freeze_panes="A5"
    for rn,s in enumerate(social,5):
        canvas="؛ ".join(f"{k}: {v}" for k,v in s.get("working_canvas",{}).items())
        vals=[s.get("platform"),s.get("account_name") or "ثبت نشده",s.get("handle") or "ثبت نشده",s.get("profile_url") or "ثبت نشده",s.get("status"),"بله" if s.get("is_official") else "خیر/تأییدنشده",s.get("avatar_asset") or "",canvas,s.get("bio") or "ندارد",s.get("evidence"),s.get("next_action")]
        for col,v in enumerate(vals,1):ws.cell(rn,col,v)
        ws.row_dimensions[rn].height=75
    style_data(ws,5,4+len(social),len(headers));add_table(ws,"SocialAccounts",4,4+len(social),len(headers))
    for i,w in enumerate([18,24,22,36,18,22,32,52,40,70,65],1):ws.column_dimensions[get_column_letter(i)].width=w
    status_format(ws,5,5,4+len(social))

    # Music catalog remains empty until source-backed records exist.
    ws=wb.create_sheet("کاتالوگ موسیقی");ws.sheet_properties.tabColor="70AD47"
    headers=["شناسه","عنوان فارسی","عنوان لاتین","نامک","نوع محتوا","شناسه هنرمند(ان)","آلبوم","تاریخ انتشار","ISRC","منبع","وضعیت حقوق","وضعیت تکمیل","یادداشت"]
    style_title(ws,"کاتالوگ موسیقی · رجیستری مستند","در منبع فعلی رکوردی از آثار واقعی وجود ندارد. نمونه‌های فایل مادر قبلی اینجا کپی نشده‌اند.",len(headers))
    for col,h in enumerate(headers,1):ws.cell(4,col,h)
    style_header(ws,4,1,len(headers));ws.freeze_panes="A5";ws.auto_filter.ref=f"A4:{get_column_letter(len(headers))}4"
    ws.merge_cells(start_row=5,start_column=1,end_row=5,end_column=len(headers));ws.cell(5,1,"رجیستری خالی است؛ رکورد جدید را پس از دریافت منبع معتبر در music-catalog/catalog.json ثبت کنید.").fill=PatternFill("solid",fgColor="FFF2CC");ws.cell(5,1).alignment=Alignment(horizontal="right",wrap_text=True);ws.row_dimensions[5].height=32
    for i,w in enumerate([20,30,28,26,18,30,25,18,20,45,25,20,50],1):ws.column_dimensions[get_column_letter(i)].width=w

    # Keep the summary first and set consistent print areas/zoom.
    wb.active=0
    for sheet in wb.worksheets:
        sheet.sheet_view.zoomScale=85
        sheet.sheet_properties.pageSetUpPr.fitToPage=True
        sheet.sheet_format.defaultRowHeight=20
        if sheet.max_row > 4 and sheet.title != "نمای کلی":
            sheet.print_title_rows="1:4"
        sheet.sheet_view.showGridLines=False
    wb.properties.title="مرکز دانش آهنگ‌بان · گزارش دیداری"
    wb.properties.subject="Brand intelligence, artist completion, visual asset index and social status"
    wb.properties.creator="Ahangban Brand Kit"
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    wb.save(OUTPUT)
    print(f"Built {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()
