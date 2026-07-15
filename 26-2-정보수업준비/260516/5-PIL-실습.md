# PIL 이미지 라이브러리 실습

압축 단원 맥락에서 PIL의 `Image` 모듈로 이미지 정보 확인, 포맷 변환, 해상도 변경을 다룬다.

## 사전 준비

```python
import os
from PIL import Image
```

- `PIL` (Pillow): 파이썬 이미지 처리 라이브러리. 코랩에는 기본 설치되어 있음
- `os`: 파일 크기 확인용 (`os.path.getsize`)

## 1. 기본: 이미지 정보 확인

이미지를 열고 확장자/해상도/파일 크기를 출력한다.

```python
im = Image.open("충남과학고.bmp")

print("이미지 확장자:", im.format)
print("이미지 해상도:", im.size)
print("파일 크기:", os.path.getsize("충남과학고.bmp"), "Bytes")
```

### 출력 예시
```
이미지 확장자: BMP
이미지 해상도: (1920, 1080)
파일 크기: 6220854 Bytes
```

### 각 값의 의미
| 속성/함수 | 의미 |
|---|---|
| `im.format` | 이미지 파일 포맷 (BMP, JPEG, PNG 등) |
| `im.size` | (가로 픽셀, 세로 픽셀) 튜플 |
| `os.path.getsize(경로)` | 파일의 실제 바이트 크기 |

`im.size`는 "이미지 안에 픽셀이 몇 개 있는가"이고, `os.path.getsize`는 "디스크에서 그 파일이 차지하는 용량"이다. 둘은 다르다.

## 2. 포맷 변환 저장

같은 이미지를 다른 포맷으로 저장하면 파일 크기가 크게 달라진다. 압축 효과를 직접 확인할 수 있다.

```python
im = Image.open("충남과학고.bmp")

# 다양한 포맷으로 저장
im.save("out.jpg")
im.save("out.png")
im.save("out.gif")

# 각 파일 크기 비교
print("BMP:", os.path.getsize("충남과학고.bmp"), "Bytes")
print("JPG:", os.path.getsize("out.jpg"), "Bytes")
print("PNG:", os.path.getsize("out.png"), "Bytes")
print("GIF:", os.path.getsize("out.gif"), "Bytes")
```

### 출력 예시 (실제 값은 이미지마다 다름)
```
BMP: 6220854 Bytes      <- 무압축
JPG:  412035 Bytes      <- 손실 압축 (가장 작음)
PNG: 1834102 Bytes      <- 무손실 압축
GIF:  524880 Bytes      <- 색상 제한 + 무손실
```

### 관찰 포인트
- **BMP**: 압축 없음. 픽셀 그대로 저장하므로 가장 큼
- **JPG**: 손실 압축. 사진 같은 풀컬러 이미지에서 매우 작음
- **PNG**: 무손실 압축. 원본 픽셀 복원 가능. JPG보다 큼
- **GIF**: 256색 팔레트 + 무손실. 단순한 이미지에 적합

해상도(`im.size`)는 그대로지만 파일 크기는 포맷마다 다르다 -> **압축의 효과**.

## 3. 해상도 변경 (resize)

`im.resize((가로, 세로))`로 픽셀 수를 줄이면 파일 크기도 줄어든다.

```python
im = Image.open("충남과학고.bmp")
print("원본 해상도:", im.size)
print("원본 크기:", os.path.getsize("충남과학고.bmp"), "Bytes")

# 가로 세로 절반으로
im_half = im.resize((im.size[0] // 2, im.size[1] // 2))
im_half.save("half.bmp")
print("축소 해상도:", im_half.size)
print("축소 크기:", os.path.getsize("half.bmp"), "Bytes")

# 가로 세로 1/4로
im_quarter = im.resize((im.size[0] // 4, im.size[1] // 4))
im_quarter.save("quarter.bmp")
print("1/4 해상도:", im_quarter.size)
print("1/4 크기:", os.path.getsize("quarter.bmp"), "Bytes")
```

### 출력 예시
```
원본 해상도: (1920, 1080)
원본 크기: 6220854 Bytes
축소 해상도: (960, 540)
축소 크기: 1555254 Bytes      <- 약 1/4
1/4 해상도: (480, 270)
1/4 크기:    388854 Bytes      <- 약 1/16
```

### 관찰 포인트
- 가로/세로를 절반으로 줄이면 픽셀 수는 1/4 (2 x 2 = 4 분의 1)
- BMP는 픽셀당 바이트 수가 고정이므로 파일 크기도 거의 1/4
- 줄어든 픽셀은 복원 불가 -> **손실 발생** (해상도 축소는 손실 압축의 한 종류로 볼 수 있음)

## 정리

| 방법 | 효과 | 손실 여부 |
|---|---|---|
| BMP -> PNG/GIF 변환 | 무손실 압축으로 크기 감소 | 무손실 |
| BMP -> JPG 변환 | 손실 압축으로 크기 크게 감소 | 손실 |
| resize로 해상도 축소 | 픽셀 수 자체를 줄여 크기 감소 | 손실 (복원 불가) |

같은 이미지여도 어떤 포맷/해상도로 저장하느냐에 따라 파일 크기가 크게 달라진다. 압축 단원에서 배운 무손실/손실 압축의 개념이 실제 이미지 파일에서도 그대로 적용됨을 확인할 수 있다.
