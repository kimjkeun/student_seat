import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def setup_korean_font():
    """한글 폰트 설정"""
    try:
        # Windows 기본 한글 폰트 사용
        font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('Korean', font_path))
            return 'Korean'
        else:
            print("한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
            return 'Helvetica'
    except:
        print("한글 폰트 설정 실패. 기본 폰트를 사용합니다.")
        return 'Helvetica'

def create_seating_chart_pdf(class_num, df, font_name='Helvetica'):
    """특정 클래스의 자리표 PDF 생성"""
    
    # 해당 클래스 학생들만 필터링
    class_students = df[df['클래스'] == class_num].copy()
    
    if class_students.empty:
        print(f"클래스 {class_num}에 학생이 없습니다.")
        return None
    
    # PDF 파일명
    filename = f'class_{class_num}_seating_chart.pdf'
    
    # PDF 문서 생성 (가로 방향)
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    story = []
    
    # 스타일 설정
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=18,
        alignment=1,  # 가운데 정렬
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=12,
        alignment=1,
        spaceAfter=15
    )
    
    # 제목 추가
    title = Paragraph(f"클래스 {class_num} 자리표", title_style)
    story.append(title)
    
    # 기본 정보
    total_students = len(class_students)
    students_with_scores = class_students['점수'].notna().sum()
    students_with_photos = class_students['파일명'].notna().sum()
    
    info_text = f"총 {total_students}명 | 성적 보유: {students_with_scores}명 | 사진 보유: {students_with_photos}명"
    info = Paragraph(info_text, subtitle_style)
    story.append(info)
    story.append(Spacer(1, 20))
    
    # 자리표 크기 결정
    max_row = class_students['행'].max()
    max_col = class_students['열'].max()
    
    # 자리표 데이터 준비
    seating_grid = {}
    for _, student in class_students.iterrows():
        row, col = student['행'], student['열']
        
        # 성적 표시
        if pd.notna(student['점수']):
            score = student['점수']
            if score >= 80:
                score_color = colors.green
            elif score >= 60:
                score_color = colors.orange
            else:
                score_color = colors.red
            score_text = f"{score:.1f}점"
        else:
            score_color = colors.grey
            score_text = "성적없음"
        
        # 사진 여부
        photo_text = "📷" if pd.notna(student['파일명']) else "❌"
        
        seating_grid[(row, col)] = {
            'name': student['이름'],
            'id': student['학번'],
            'score_text': score_text,
            'score_color': score_color,
            'photo': photo_text
        }
    
    # 자리표 테이블 생성
    table_data = []
    
    for row in range(1, max_row + 1):
        row_data = []
        for col in range(1, max_col + 1):
            if (row, col) in seating_grid:
                student = seating_grid[(row, col)]
                # 각 자리에 학번, 이름, 성적을 3줄로 표시
                cell_content = f"{student['id']}\n{student['name']}\n{student['score_text']}"
                row_data.append(cell_content)
            else:
                row_data.append("")
        table_data.append(row_data)
    
    # 교탁 행 추가
    teacher_row = ["교탁"] + [""] * (max_col - 1)
    table_data.append(teacher_row)
    
    # 테이블 생성
    table = Table(table_data)
    
    # 테이블 스타일 설정
    table_style = [
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, max_row), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 0), (-1, max_row), [colors.white, colors.lightgrey]),
    ]
    
    # 성적에 따른 색상 적용
    for row in range(1, max_row + 1):
        for col in range(1, max_col + 1):
            if (row, col) in seating_grid:
                student = seating_grid[(row, col)]
                table_style.append(('TEXTCOLOR', (col-1, row-1), (col-1, row-1), student['score_color']))
    
    # 교탁 스타일
    table_style.extend([
        ('BACKGROUND', (0, max_row), (-1, max_row), colors.yellow),
        ('FONTSIZE', (0, max_row), (-1, max_row), 14),
        ('SPAN', (0, max_row), (-1, max_row)),
    ])
    
    table.setStyle(TableStyle(table_style))
    story.append(table)
    
    story.append(Spacer(1, 30))
    
    # 범례 추가
    legend_style = ParagraphStyle(
        'Legend',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leftIndent=50
    )
    
    legend_text = """
    <b>범례:</b><br/>
    <font color="green">● 우수 (80점 이상)</font><br/>
    <font color="orange">● 보통 (60-79점)</font><br/>
    <font color="red">● 개선필요 (60점 미만)</font><br/>
    <font color="grey">● 성적없음</font><br/>
    📷 사진있음 | ❌ 사진없음
    """
    
    legend = Paragraph(legend_text, legend_style)
    story.append(legend)
    
    story.append(Spacer(1, 20))
    
    # 통계 정보 추가
    stats_style = ParagraphStyle(
        'Stats',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        leftIndent=50
    )
    
    scores = class_students['점수'].dropna()
    if len(scores) > 0:
        avg_score = scores.mean()
        max_score = scores.max()
        min_score = scores.min()
        
        excellent = len(scores[scores >= 80])
        good = len(scores[(scores >= 60) & (scores < 80)])
        needs_improvement = len(scores[scores < 60])
        
        stats_text = f"""
        <b>성적 통계:</b><br/>
        • 평균 성적: {avg_score:.1f}점<br/>
        • 최고 성적: {max_score:.1f}점 | 최저 성적: {min_score:.1f}점<br/>
        • 성적 분포: 우수 {excellent}명, 보통 {good}명, 개선필요 {needs_improvement}명
        """
        
        stats = Paragraph(stats_text, stats_style)
        story.append(stats)
    
    # PDF 생성
    doc.build(story)
    return filename

def create_all_class_pdfs():
    """모든 클래스의 자리표 PDF 생성"""
    
    print("="*60)
    print("              클래스별 자리표 PDF 생성기")
    print("="*60)
    
    # 한글 폰트 설정
    font_name = setup_korean_font()
    
    # 데이터 로드
    try:
        df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
        print(f"✅ 데이터 로드 완료: {len(df)}명의 학생 정보")
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        return
    
    # 클래스 목록 확인
    classes = sorted(df['클래스'].unique())
    print(f"📚 발견된 클래스: {classes}")
    print()
    
    created_files = []
    
    # 각 클래스별 PDF 생성
    for class_num in classes:
        print(f"📄 클래스 {class_num} PDF 생성 중...")
        
        try:
            filename = create_seating_chart_pdf(class_num, df, font_name)
            if filename:
                created_files.append(filename)
                print(f"✅ {filename} 생성 완료")
        except Exception as e:
            print(f"❌ 클래스 {class_num} PDF 생성 실패: {e}")
    
    print(f"\n{'='*60}")
    print("                PDF 생성 완료!")
    print(f"{'='*60}")
    
    if created_files:
        print("📁 생성된 파일:")
        for filename in created_files:
            file_size = os.path.getsize(filename) / 1024  # KB
            print(f"  • {filename} ({file_size:.1f} KB)")
        
        print(f"\n💡 사용법:")
        print(f"  • PDF 파일을 열어서 자리표를 확인하세요")
        print(f"  • 인쇄해서 교실에서 사용할 수 있습니다")
        print(f"  • 성적은 색상으로 구분되어 있습니다 (녹색: 우수, 주황: 보통, 빨강: 개선필요)")
    else:
        print("❌ 생성된 파일이 없습니다.")

if __name__ == "__main__":
    create_all_class_pdfs()
