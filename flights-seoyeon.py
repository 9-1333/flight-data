
from nycflights13 import flights, planes
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


'''
주제 자유
merge 사용해서 flgihts와 plaens 병합한 데이터로
각 데이터 변수 최소 하나씩 선택 후 분석할 것
날짜시간 전처리 코드 들어갈 것
문자열 전처리 코드 들어갈 것
시각화 종류 최소 3개 (배우지 않을 것도 할 수 있음 넣어도 ㅇㅇ)
'''

# 데이터 확인
flights.info()
planes.info()


# flights, planes 병합
data = pd.merge(flights, planes, on = "tailnum", how = "left")
data.info()




'''Q. 엔진 개수가 많을수록 좌석수가 많아질까? (여객기가 클까?)'''
# 1) 꺾은선 그래프로 엔진 개수별 평균 좌석수 확인
engines_seats = data.groupby('engines')['seats'].mean()
engines_seats

plt.figure(figsize=(8, 5))
plt.plot(engines_seats.index, engines_seats.values, marker='o', linestyle='-', color='b')

# 각 점에 라벨 추가
for i, txt in enumerate(engines_seats.values):
    if engines_seats.index[i] == 1.0:
        plt.text(engines_seats.index[i] + 0.1, txt, f"{txt:.1f}", ha='left', fontsize=10, color="black")  # 엔진 1개짜리는 오른쪽
    else:
        plt.text(engines_seats.index[i] - 0.1, txt, f"{txt:.1f}", ha='right', fontsize=10, color="black")  # 나머지는 왼쪽

# 축과 제목 설정
plt.xticks(engines_seats.index) 
plt.xlabel("Number of Engines")
plt.ylabel("Average Seats")
plt.title("Average Seats by Number of Engines")
plt.grid(True, linestyle="--", alpha=0.7)

plt.show()

'1 -> 2 -> 3개로 갈수록 좌석수가 늘긴하지만, 엔진 4개부터는 갑자기 좌석수 감소'
'이상치의 영향이 과하게 반영된 건지 확인해보자'




# 2) 박스 플롯으로 엔진 개수별 분포 확인
# 2-1) 박스 플롯
plt.figure(figsize=(8, 5))
sns.boxplot(x="engines", y="seats", data=data, hue="engines", palette="Blues", width=0.5)
plt.xlabel("Number of Engines")
plt.ylabel("Seats")
plt.title("Seats Distribution by Number of Engines")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

'엔진 3개, 4개일 때는 왜 이렇게 뜨는건지 산점도로 개별적인 분포를 확인해야겠다'


# 2-2) 박스플롯에 산점도 추가
plt.figure(figsize=(8, 5))
sns.boxplot(x="engines", y="seats", data=data, hue="engines", palette="Blues", width=0.5)

# 엔진 3개, 4개짜리만 따로 필터링해서 산점도 추가
sns.stripplot(x="engines", y="seats", data=data[(data["engines"] >= 3)], 
              color="red", alpha=0.5, jitter=True, size=8)

# 라벨 & 스타일 설정
plt.xlabel("Number of Engines")
plt.ylabel("Seats")
plt.title("Seats Distribution by Number of Engines")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.show()

'''해석
엔진 3개 → 좌석 수가 400명 넘는 항공기 vs 0~10명짜리 항공기 같이 존재 (극단적인 차이!)
엔진 4개 → 처음 가설에 따르면 박스플롯의 사각형이 2개일때보다 더 높이 있어야 되는데,
오히려 사각형의 위치가 좌석수 0-100에 분포
(0-10명 // 100명 항공기)
'''
# → 여기서 "왜 4개짜리인데 사람이 적게 탈까?"라는 의문이 생김.
# ㄴ 추측 1: 4개짜리 엔진 중 일부는 대형 화물기일 가능성이 있음 (화물기는 좌석 수 X).
# ㄴ 추측 2: 군용기, 전세기 같은 특수 목적기일 수도 있음.

data.loc[data("model") == "CF-5D"]

data["engines"].value_counts()
# 3) 엔진 3개, 4개면서 좌석수가 적은 항공기 확인
# 3-1) 엔진이 세개인데, 좌석이 50명 이하인 경우의 모델
data.loc[(data['engines'] == 3) & (data['seats'] <= 50)] # MYSTERE FALCON 900
# 검색해보니 비즈니스 제트기 -> 전세기라서 좌석수가 적었구나


# 2) 엔진이 네개인데, 좌석이 50명 이하인 경우의 모델
data.loc[(data['engines'] == 4) & (data['seats'] <= 150), 'model']
data.loc[(data['engines'] == 4) & (data['seats'] <= 150), 'model'].value_counts() # CF-5D / DC-7BF
# 검색해보니 캐나다 공군이 운용한 전투기


'''
MYSTERE FALCON 900: 비즈니스 제트기
https://www.dassault-aviation.com/en/passion/aircraft/civil-dassault-aircraft/falcon-900/

CF-5D: 

DC-78F:





결론: 엔진 개수가 많다고 꼭 좌석이 많아지는 건 아니고,
특수한 용도의 항공기(화물기, 군용기, VIP기 등)도 존재한다.
'''


del filtered_data

filtered_data = data.loc[
    (data['engines'] >= 3) & (data['seats'] <= 150), 
    ['engines', 'manufacturer', 'model', 'seats']
]
filtered_data = filtered_data.drop_duplicates(subset=['model'])
import ace_tools as tools  
tools.display_dataframe_to_user(name="Filtered Aircraft Data", dataframe=filtered_data)
filtered_data = filtered_data.drop_duplicates(subset=['model'])

# 2️⃣ 모델별 개수(count) 계산
filtered_data['count'] = filtered_data['model'].value_counts().reset_index()
model_counts.columns = ['model', 'count']

# 3️⃣ 원본 데이터와 모델별 개수 합치기 (모델 이름 기준)
final_df = filtered_data.merge(model_counts, on='model')

# 4️⃣ 중복 제거 (같은 모델이면 한 번만 표시)
final_df = final_df.drop_duplicates(subset=['model']).sort_values(by='count', ascending=False)



# 이상한 비행기 모델
# weird_planes = data[(data["engines"] >= 3) & (data["seats"] <= 130)]
# import seaborn as sns
# plt.figure(figsize=(10, 5))
# sns.countplot(y=weird_planes["model"], order=weird_planes["model"].value_counts().index, palette="coolwarm")
# plt.xlabel("Count")
# plt.ylabel("Aircraft Model")
# plt.title("Unusual Aircraft Models with 3+ Engines and ≤50 Seats")
# plt.show()




# 1개짜리(단발기) → 경비행기, 개인용 소형기 (좌석 수 적음, 평균 4명)
# 2개짜리(쌍발기) → 가장 일반적인 여객기 (평균 137명)
# 3개짜리(삼발기) → 중대형 비행기일 것으로 보였지만, 데이터상으론 소수 (평균 169명)
# 4개짜리(사발기) → 대형 여객기일 줄 알았는데 좌석 수가 67명?

''''''

engines_seats.items()




'''엔진 개수별 엔진 종류'''
# 데이터를 보면 엔진 2개짜리 비행기가 제일 많아서 엔진 2개짜리가 가장 일반적인 것 같음
# 특히 "Turbofan" 엔진이 압도적으로 많음
# -> 즉, 상용 여객기 대부분은 2개짜리 터보팬 엔진 사용.
# B737, A320 같은 단거리~중거리용 여객기들이 다 여기 속할 가능성이 높음.
# 현대 민간 여객기는 대부분 엔진 2개(쌍발기)가 일반적이다!
# (연료 효율과 경제성 때문에 4발기보다 2발기를 선호하는 추세)
data.groupby('engines')['engine'].value_counts()


# 엔진 하나일 때) 레시프로 엔진
engine_name = data.loc[data['engines'] == 1.0]['engine'].value_counts().keys()
engine_counts = data.loc[data['engines'] == 1.0]['engine'].value_counts().values

plt.pie(engine_counts, labels = engine_name, autopct = '%.1f%%')
plt.show()


# 엔진 두개일 때 ....
engine_name2 = data.loc[data['engines'] == 2.0]['engine'].value_counts().keys()
engine_counts2 = data.loc[data['engines'] == 2.0]['engine'].value_counts().values

plt.pie(engine_counts2, labels = engine_name2, autopct = '%.1f%%')
plt.show()


# nycflights13 내 3발기
engine_name3 = data.loc[data['engines'] == 3.0]['engine'].value_counts().keys()
engine_counts3 = data.loc[data['engines'] == 3.0]['engine'].value_counts().values

plt.pie(engine_counts3, labels = engine_name3, autopct = '%.1f%%')
plt.show()


# nycflights13 내 4발기
engine_name4 = data.loc[data['engines'] == 4.0]['engine'].value_counts().keys()
engine_counts4 = data.loc[data['engines'] == 4.0]['engine'].value_counts().values

plt.pie(engine_counts4, labels = engine_name4, autopct = '%.1f%%')
plt.show()


data[data["engines"] == 4]["seats"].describe()
data[data["engines"] == 3]["seats"].describe()

0.5*0.01 / 0.017

