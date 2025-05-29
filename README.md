# Dự đoán lượng calo đốt khi tập luyện dựa trên thể trạng và thời gian tập luyện

## I. Giới thiệu

+ Dự án này nhằm xây dựng một mô hình học máy để dự đoán lượng calo tiêu thụ trong quá trình tập luyện, dựa trên các thông tin cá nhân và yếu tố thể chất như thời gian tập, nhịp tim và nhiệt độ cơ thể.

## II. Dữ liệu sử dụng
Dữ liệu được thu thập từ Kaggle, bao gồm:

+ calories.csv: Chứa thông tin về lượng calo tiêu thụ của 15.000 người tập luyện.

+ exercise.csv: Chứa thông tin cá nhân như tuổi, chiều cao, cân nặng, thời gian tập luyện, nhịp tim và nhiệt độ cơ thể.

## III. Quy trình phát triển
### 1. Tiền xử lý dữ liệu
+ Loại bỏ dữ liệu trùng lặp và không cần thiết.
+ Chuẩn hóa dữ liệu (ví dụ: chuyển đổi giới tính thành dạng số).
+ Chia tập dữ liệu thành train và test với tỷ lệ 80-20%.

### 2. Phân tích và trực quan hóa dữ liệu
+ Đánh giá sự phân bố của từng thuộc tính.
+ Phân tích mức độ tương quan giữa các yếu tố và lượng calo tiêu thụ.
  
### 3. Huấn luyện mô hình
Sử dụng ba mô hình chính:
+ Linear Regression: Đơn giản, dễ hiểu, nhưng kém hiệu quả hơn.
+ Random Forest Regressor: Xử lý dữ liệu phi tuyến tốt, tránh overfitting.
+ XGBoost Regressor: Hiệu suất cao, tối ưu hóa tốt nhất.
### 4. Đánh giá mô hình
Các chỉ số đánh giá:
+ R-squared score (Độ phù hợp của mô hình)
+ Mean Absolute Error (MAE) (Sai số trung bình tuyệt đối)
+ Cross-validation score (Kiểm tra tính ổn định của mô hình)

5. Giao diện phần mềm dự đoán calories
![Screenshot (448)](https://github.com/user-attachments/assets/261f6e3b-48fe-4c5a-87bc-87e35f211ae1)
![Screenshot (449)](https://github.com/user-attachments/assets/8eb5ef9a-2c52-4e4f-9a83-9eb716156e2d)
![Screenshot (450)](https://github.com/user-attachments/assets/873faa10-7226-4bc8-af6b-6882a9abfccd)
![Screenshot (451)](https://github.com/user-attachments/assets/df09a3d0-ef6d-4aff-8f0f-698c3554cc7e)
![Screenshot (453)](https://github.com/user-attachments/assets/d0220048-9436-4701-bdd9-4fc29fb78455)
![Screenshot (454)](https://github.com/user-attachments/assets/ea3463cf-da03-4cb7-ae2a-a41a513dd6fb)
![Screenshot (455)](https://github.com/user-attachments/assets/037dcf10-2416-4369-98d3-77c3a89c833f)


