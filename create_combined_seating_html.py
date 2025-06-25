import pandas as pd
import os
from pathlib import Path

def create_combined_seating_chart_html(df):
    """모든 클래스의 자리표를 하나의 HTML 파일로 통합"""
    
    # 클래스 목록 가져오기
    classes = sorted(df['클래스'].unique())
    
    # HTML 시작 부분
    html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전체 클래스 자리표</title>
    <style>
        body {
            font-family: 'Malgun Gothic', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .header {
            text-align: center;
            margin-bottom: 0;
            background: white;
            padding: 15px 20px 10px 20px;
            border-radius: 10px 10px 0 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #2c3e50;
            margin: 0;
            font-size: 1.8em;
        }
        
        /* 탭 스타일 */
        .tab-container {
            background: white;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            overflow: hidden;
        }
        
        .tab-buttons {
            display: flex;
            background: #ecf0f1;
        }
        
        .tab-button {
            flex: 1;
            padding: 15px 20px;
            background: #ecf0f1;
            border: none;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: bold;
            color: #7f8c8d;
            transition: all 0.3s ease;
        }
        
        .tab-button:hover {
            background: #d5dbdb;
        }
        
        .tab-button.active {
            background: #3498db;
            color: white;
        }
        
        .tab-content {
            display: none;
            padding: 20px;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .seating-container {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }
        
        .seating-table {
            border-collapse: separate;
            border-spacing: 10px;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .seat {
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
            cursor: pointer;
        }
        
        .seat:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        .seat.excellent {
            border-color: #27ae60;
            background: linear-gradient(135deg, #ffffff 0%, #f8fff8 100%);
        }
        
        .seat.good {
            border-color: #f39c12;
            background: linear-gradient(135deg, #ffffff 0%, #fffdf8 100%);
        }
        
        .seat.needs {
            border-color: #e74c3c;
            background: linear-gradient(135deg, #ffffff 0%, #fff8f8 100%);
        }
        
        .seat.none {
            border-color: #95a5a6;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        }
        
        .student-photo {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            object-fit: cover;
            margin: 2px auto 5px;
            border: 2px solid #fff;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            display: block;
        }
        
        .no-photo {
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
        }
        
        .student-id {
            font-size: 0.8em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 3px;
            line-height: 1.1;
        }
        
        .student-score {
            font-size: 0.75em;
            font-weight: bold;
            padding: 1px 4px;
            border-radius: 10px;
            display: inline-block;
        }
        
        .excellent .student-score {
            background: #27ae60;
            color: white;
        }
        
        .good .student-score {
            background: #f39c12;
            color: white;
        }
        
        .needs .student-score {
            background: #e74c3c;
            color: white;
        }
        
        .none .student-score {
            background: #95a5a6;
            color: white;
        }
        
        /* 이미지 모달 스타일 */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.8);
            animation: fadeIn 0.3s;
        }
        
        .modal-content {
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
        }
        
        .modal-image {
            max-width: 300px;
            max-height: 400px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .modal-info {
            margin-top: 15px;
            font-size: 1.2em;
            color: #2c3e50;
        }
        
        .close {
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 28px;
            font-weight: bold;
            color: #aaa;
            cursor: pointer;
        }
        
        .close:hover {
            color: #000;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* 비밀번호 인증 스타일 */
        .password-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        
        .password-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 400px;
            width: 90%;
        }
        
        .password-container h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .password-input {
            width: 100%;
            padding: 15px;
            font-size: 1.2em;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            box-sizing: border-box;
        }
        
        .password-input:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .password-button {
            background: #3498db;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.1em;
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .password-button:hover {
            background: #2980b9;
        }
        
        .password-error {
            color: #e74c3c;
            margin-top: 10px;
            display: none;
        }
        
        .main-content {
            display: none;
        }
        
        @media print {
            body { margin: 0; }
            .password-overlay { display: none !important; }
            .main-content { display: block !important; }
            .tab-container { 
                box-shadow: none;
                margin-bottom: 0;
            }
            .tab-buttons { display: none; }
            .tab-content { 
                display: none !important;
                padding: 0;
            }
            .tab-content.active { 
                display: block !important;
            }
            .seating-table { 
                page-break-inside: avoid;
                box-shadow: none;
            }
            .modal { display: none !important; }
            .header {
                box-shadow: none;
                margin-bottom: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="password-overlay">
        <div class="password-container">
            <h2>비밀번호 인증</h2>
            <input type="password" class="password-input" id="password-input" placeholder="비밀번호를 입력하세요">
            <button class="password-button" id="password-button">인증</button>
            <div class="password-error" id="password-error"></div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="header">
            <h1>🏫 전체 클래스 자리표</h1>
        </div>
        
        <div class="tab-container">
            <div class="tab-buttons">
"""
    
    # 탭 버튼 생성
    for i, class_num in enumerate(classes):
        active_class = "active" if i == 0 else ""
        html_content += f'            <button class="tab-button {active_class}" onclick="showTab({class_num})">{class_num}반</button>\n'
    
    html_content += """        </div>
"""
    
    # 각 클래스별 탭 콘텐츠 생성
    for i, class_num in enumerate(classes):
        active_class = "active" if i == 0 else ""
        html_content += f"""
        <div id="class-{class_num}" class="tab-content {active_class}">
            <div class="seating-container">
                <table class="seating-table">
"""
        
        # 해당 클래스 학생들만 필터링
        class_students = df[df['클래스'] == class_num].copy()
        
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
        
        # 자리표 테이블 생성
        for row in range(1, max_row + 1):
            # 해당 행에 학생이 있는지 확인
            has_students_in_row = any((row, col) in seating_grid for col in range(1, max_col + 1))
            
            # 학생이 있는 행만 출력
            if has_students_in_row:
                html_content += "                    <tr>\n"
                
                for col in range(1, max_col + 1):
                    if (row, col) in seating_grid:
                        student = seating_grid[(row, col)]
                        
                        # 이미지 HTML
                        if student['image_path'] and os.path.exists(student['image_path']):
                            image_html = f'<img src="{student["image_path"]}" alt="{student["name"]}" class="student-photo">'
                        else:
                            image_html = '<div class="no-photo">👤</div>'
                        
                        html_content += f"""                        <td class="seat {student['score_class']}">
                            {image_html}
                            <div class="student-id">{student['id']}</div>
                            <div class="student-score">{student['score_emoji']} {student['score_text']}</div>
                        </td>
"""
                    else:
                        html_content += '                        <td class="seat"></td>\n'
                
                html_content += "                    </tr>\n"
        
        html_content += """                </table>
            </div>
        </div>
"""
    
    html_content += """    </div>
    </div>
    
    <!-- 이미지 모달 -->
    <div id="imageModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <img id="modalImage" class="modal-image" src="" alt="">
            <div id="modalInfo" class="modal-info"></div>
        </div>
    </div>
    
    <script>
        // 탭 전환 함수
        function showTab(classNum) {
            // 모든 탭 버튼과 콘텐츠 비활성화
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            // 선택된 탭 활성화
            event.target.classList.add('active');
            document.getElementById(`class-${classNum}`).classList.add('active');
        }
        
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
        
        // 비밀번호 인증
        const passwordInput = document.getElementById('password-input');
        const passwordButton = document.getElementById('password-button');
        const passwordError = document.getElementById('password-error');
        const mainContent = document.querySelector('.main-content');
        const passwordOverlay = document.querySelector('.password-overlay');
        
        passwordButton.addEventListener('click', function() {
            const password = passwordInput.value.trim();
            if (password === '1679') {
                mainContent.style.display = 'block';
                passwordOverlay.style.display = 'none';
            } else {
                passwordError.style.display = 'block';
                passwordError.textContent = '잘못된 비밀번호입니다.';
                passwordInput.value = '';
                passwordInput.focus();
            }
        });
        
        // Enter 키로 비밀번호 인증
        passwordInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                passwordButton.click();
            }
        });
        
        // 페이지 로드 시 비밀번호 입력창에 포커스
        passwordInput.focus();
    </script>
</body>
</html>
"""
    
    # HTML 파일 저장
    filename = 'all_classes_seating_chart.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size = os.path.getsize(filename) / 1024  # KB 단위
    print(f"✅ {filename} 생성 완료 ({file_size:.1f} KB)")
    
    return filename

def main():
    """메인 함수"""
    print("=" * 60)
    print("              통합 자리표 HTML 생성기")
    print("=" * 60)
    
    # 데이터 로드
    try:
        df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
        print(f"✅ 데이터 로드 완료: {len(df)}명의 학생 정보")
        
        classes = sorted(df['클래스'].unique())
        print(f"📚 발견된 클래스: {classes}")
        
        # 통합 HTML 생성
        print("\n🌐 통합 자리표 HTML 생성 중...")
        filename = create_combined_seating_chart_html(df)
        
        print("\n" + "=" * 60)
        print("                HTML 생성 완료!")
        print("=" * 60)
        print(f"🌐 생성된 파일: {filename}")
        print("\n💡 사용법:")
        print("  • HTML 파일을 브라우저에서 열어 자리표를 확인하세요")
        print("  • 상단 탭을 클릭하여 클래스를 전환할 수 있습니다")
        print("  • 학생 사진을 클릭하면 큰 이미지를 볼 수 있습니다")
        print("  • Ctrl+P로 인쇄할 수 있습니다")
        print("  • 성적에 따라 색상이 구분되어 있습니다")
        
    except FileNotFoundError:
        print("❌ integrated_student_data.csv 파일을 찾을 수 없습니다.")
        print("   먼저 데이터 통합을 실행해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
