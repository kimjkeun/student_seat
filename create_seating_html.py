import pandas as pd
import os
from pathlib import Path

def create_seating_chart_html(class_num, df):
    """특정 클래스의 자리표 HTML 생성"""
    
    # 해당 클래스 학생들만 필터링
    class_students = df[df['클래스'] == class_num].copy()
    
    if class_students.empty:
        print(f"클래스 {class_num}에 학생이 없습니다.")
        return None
    
    # HTML 파일명
    filename = f'class_{class_num}_seating_chart.html'
    
    # 자리표 크기 결정
    max_row = class_students['행'].max()
    max_col = class_students['열'].max()
    
    # 자리표 데이터 준비
    seating_grid = {}
    for _, student in class_students.iterrows():
        row, col = student['행'], student['열']
        
        # 성적에 따른 색상 클래스
        if pd.notna(student['점수']):
            score = student['점수']
            if score >= 80:
                score_class = "excellent"
                score_emoji = "🌟"
            elif score >= 60:
                score_class = "good"
                score_emoji = "👍"
            else:
                score_class = "needs"
                score_emoji = "💪"
            score_text = f"{score:.0f}"
        else:
            score_class = "none"
            score_emoji = "❓"
            score_text = "-"
        
        # 이미지 경로 확인
        image_path = ""
        if pd.notna(student['파일명']):
            # 상대 경로로 이미지 찾기
            possible_paths = [
                f"image/class_{class_num}/{student['파일명']}",
                f"student_images/{student['파일명']}",
                f"image/{student['파일명']}"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    image_path = path
                    break
        
        # 학번에서 반 번호 추출 (3XXYY 형태에서 XX 부분)
        student_id = str(student['학번'])
        if len(student_id) >= 4 and student_id.startswith('3'):
            class_number = str(int(student_id[1:3]))  # int로 변환하여 앞의 0 제거
        else:
            class_number = str(class_num)
        
        seating_grid[(row, col)] = {
            'id': f"{class_number}반 {student['이름']}",
            'name': student['이름'],
            'score_text': score_text,
            'score_class': score_class,
            'score_emoji': score_emoji,
            'image_path': image_path,
            'has_photo': pd.notna(student['파일명'])
        }
    
    # HTML 생성
    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>클래스 {class_num} 자리표</title>
    <style>
        body {{
            font-family: 'Malgun Gothic', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }}
        
        .stats {{
            margin: 10px 0;
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .seating-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }}
        
        .seating-table {{
            border-collapse: separate;
            border-spacing: 10px;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .seat {{
            width: 120px;
            height: 110px;
            border: 2px solid #ddd;
            border-radius: 8px;
            text-align: center;
            vertical-align: top;
            padding: 5px 5px 2px 5px;
            background: white;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .seat:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        .seat.excellent {{
            border-color: #27ae60;
            background: linear-gradient(135deg, #ffffff 0%, #f8fff8 100%);
        }}
        
        .seat.good {{
            border-color: #f39c12;
            background: linear-gradient(135deg, #ffffff 0%, #fffdf8 100%);
        }}
        
        .seat.needs {{
            border-color: #e74c3c;
            background: linear-gradient(135deg, #ffffff 0%, #fff8f8 100%);
        }}
        
        .seat.none {{
            border-color: #95a5a6;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        }}
        
        .student-photo {{
            width: 50px;
            height: 50px;
            border-radius: 12px;
            object-fit: cover;
            margin: 2px auto 5px;
            border: 2px solid #fff;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            display: block;
        }}
        
        .no-photo {{
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: #ecf0f1;
            margin: 2px auto 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
            color: #bdc3c7;
        }}
        
        .student-id {{
            font-size: 0.8em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 3px;
            line-height: 1.1;
        }}
        
        .student-score {{
            font-size: 0.75em;
            font-weight: bold;
            padding: 1px 4px;
            border-radius: 10px;
            display: inline-block;
        }}
        
        .excellent .student-score {{
            background: #27ae60;
            color: white;
        }}
        
        .good .student-score {{
            background: #f39c12;
            color: white;
        }}
        
        .needs .student-score {{
            background: #e74c3c;
            color: white;
        }}
        
        .none .student-score {{
            background: #95a5a6;
            color: white;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.8);
            animation: fadeIn 0.3s;
        }}
        
        .modal-content {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-width: 90%;
            max-height: 90%;
        }}
        
        .modal-image {{
            max-width: 300px;
            max-height: 400px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .modal-info {{
            margin-top: 15px;
            font-size: 1.2em;
            color: #2c3e50;
        }}
        
        .close {{
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 28px;
            font-weight: bold;
            color: #aaa;
            cursor: pointer;
        }}
        
        .close:hover {{
            color: #000;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @media print {{
            body {{ margin: 0; }}
            .seating-table {{ page-break-inside: avoid; }}
            .modal {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏫 클래스 {class_num} 자리표</h1>
    </div>
    
    <div class="seating-container">
        <table class="seating-table">
"""
    
    # 자리표 테이블 생성
    for row in range(1, max_row + 1):
        # 해당 행에 학생이 있는지 확인
        has_students_in_row = any((row, col) in seating_grid for col in range(1, max_col + 1))
        
        # 학생이 있는 행만 출력
        if has_students_in_row:
            html_content += "            <tr>\n"
            
            for col in range(1, max_col + 1):
                if (row, col) in seating_grid:
                    student = seating_grid[(row, col)]
                    
                    # 이미지 HTML
                    if student['image_path'] and os.path.exists(student['image_path']):
                        image_html = f'<img src="{student["image_path"]}" alt="{student["name"]}" class="student-photo">'
                    else:
                        image_html = '<div class="no-photo">👤</div>'
                    
                    html_content += f"""
                    <td class="seat {student['score_class']}">
                        {image_html}
                        <div class="student-id">{student['id']}</div>
                        <div class="student-score">{student['score_emoji']} {student['score_text']}</div>
                    </td>
    """
                else:
                    html_content += '                <td class="seat"></td>\n'
            
            html_content += "            </tr>\n"
    
    html_content += f"""
        </table>
    </div>
    
    <!-- 이미지 모달 -->
    <div id="imageModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <img id="modalImage" class="modal-image" src="" alt="">
            <div id="modalInfo" class="modal-info"></div>
        </div>
    </div>
"""
    
    # JavaScript 코드 추가
    html_content += """
    <script>
        // 모달 관련 요소들
        const modal = document.getElementById('imageModal');
        const modalImage = document.getElementById('modalImage');
        const modalInfo = document.getElementById('modalInfo');
        const closeBtn = document.querySelector('.close');
        
        // 자리 클릭 시 학생 정보 강조 및 이미지 모달
        document.querySelectorAll('.seat:not(:empty)').forEach(seat => {
            seat.addEventListener('click', function() {
                // 기존 강조 제거
                document.querySelectorAll('.seat').forEach(s => s.style.transform = '');
                
                // 클릭된 자리 강조
                this.style.transform = 'scale(1.05)';
                
                // 이미지가 있는 경우 모달 표시
                const img = this.querySelector('.student-photo');
                if (img) {
                    modalImage.src = img.src;
                    modalImage.alt = img.alt;
                    
                    const studentId = this.querySelector('.student-id').textContent;
                    const studentScore = this.querySelector('.student-score').textContent;
                    modalInfo.innerHTML = `<strong>${studentId}</strong><br>성적: ${studentScore}`;
                    
                    modal.style.display = 'block';
                }
                
                // 3초 후 강조 해제
                setTimeout(() => {
                    this.style.transform = '';
                }, 3000);
            });
        });
        
        // 모달 닫기
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
        
        // 모달 배경 클릭 시 닫기
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
        
        // ESC 키로 모달 닫기
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                modal.style.display = 'none';
            }
        });
        
        // 인쇄 기능
        function printSeatingChart() {
            window.print();
        }
        
        // 키보드 단축키 (Ctrl+P)
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                printSeatingChart();
            }
        });
    </script>
</body>
</html>
"""
    
    # HTML 파일 저장
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def create_all_class_htmls():
    """모든 클래스의 자리표 HTML 생성"""
    
    print("="*60)
    print("              클래스별 자리표 HTML 생성기")
    print("="*60)
    
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
    
    # 각 클래스별 HTML 생성
    for class_num in classes:
        print(f"🌐 클래스 {class_num} HTML 생성 중...")
        
        try:
            filename = create_seating_chart_html(class_num, df)
            if filename:
                created_files.append(filename)
                print(f"✅ {filename} 생성 완료")
        except Exception as e:
            print(f"❌ 클래스 {class_num} HTML 생성 실패: {e}")
    
    print(f"\n{'='*60}")
    print("                HTML 생성 완료!")
    print(f"{'='*60}")
    
    if created_files:
        print("🌐 생성된 파일:")
        for filename in created_files:
            file_size = os.path.getsize(filename) / 1024  # KB
            print(f"  • {filename} ({file_size:.1f} KB)")
        
        print(f"\n💡 사용법:")
        print(f"  • HTML 파일을 브라우저에서 열어 자리표를 확인하세요")
        print(f"  • 학생 사진과 함께 이름, 성적을 확인할 수 있습니다")
        print(f"  • 자리를 클릭하면 해당 학생이 강조됩니다")
        print(f"  • Ctrl+P로 인쇄할 수 있습니다")
        print(f"  • 성적에 따라 색상이 구분되어 있습니다")
    else:
        print("❌ 생성된 파일이 없습니다.")

if __name__ == "__main__":
    create_all_class_htmls()
