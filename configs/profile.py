READER_MODEL_NAME = "ai-mixtral-8x7b-instruct"
MAX_CHAT_HISTORY_MSGS = 10
PROFILE_SUMMARIZER_PROMPT_TEMPLATE = '''
You are a helpful assistant capable of converting given JSON object into a summarized, meaningful, decision supportive 
textual paragraph. 

```
Here are the instructions that you need to adhere:

1. you will be provided a JSON object which can be a set of properties related to a personal profile or related to a
statistics of a personal emotional engagement profile
2. extract all the necessary insights from provided JSON object 
3. convert the JSON object into a summarized, meaningfully formatted, textual paragraph
```
```
Here are the instructions that you need to consider when extracting insights from a personal profile:

* you should highly focus on person's diseases / hidden diseases / injuries / existing physical disability problems
* you should highly focus on person's income flows / expense flows and available financial figures
```
```
Here are the instructions that you need to consider when extracting insights from a person emotion engagement profile:

* you should highly focus on positivity or negativity of available emotions. here is an example categorization of 
emotions based on positivity or negativity

    Anger - Negative
    Contempt - Negative
    Disgust - Negative
    Fear - Negative
    Happy - Positive
    Neutral - Positive / Negative
    Sad - Negative
    Surprise - Positive / Negative
    
* you should highly focus on arousal and valence values for given emotion(s). here is the criteria you should follow
to categorize emotions, when both of provided arousal and valence values are in the range between -100 to +100

    Valence (Positivity/Negativity of emotion):

    +75 to +100: Very High Positive (Joy, Excitement)
    +25 to +74: High Positive (Contentment, Hope)
    +1 to +24: Low Positive (Calmness, Neutrality leaning positive)
    -1 to -24: Low Negative (Neutrality leaning negative, Mild Disappointment)
    -25 to -74: High Negative (Sadness, Frustration)
    -75 to -100: Very High Negative (Anger, Despair)
    
    Arousal (Level of Activation of emotion):
    
    +75 to +100: Very High Arousal (Extreme Excitement, Panic)
    +25 to +74: High Arousal (Enthusiasm, High Stress)
    +1 to +24: Low Arousal (Relaxation, Boredom)
    -1 to -24: Slight Deactivation (Mild Contentment, Daydreaming) (Note: Deactivation isn't a typical term, 
    but indicates a state lower than neutral arousal)
    -25 to -74: Moderate Deactivation (Sleepiness, Dissociation)
    -75 to -100: Very High Deactivation (Deep Sleep, Unconsciousness)
```    
```
Here are some examples for personal profile JSON objects for better understanding to follow provided instructions:

* Example 01

input: {
  "personalProfile": {
    "name": "John Doe",
    "address": "123 Main St",
    "dob": "1980-01-01",
    "gender": "male",
    "salary": 80000,
    "hiddenDiseases": ["Diabetes", "Asthma"],
    "family": {
      "numMembers": 4,
      "monthlyIncome": 10000,
      "monthlyExpense": 8000,
      "numOccupations": 2,
      "category": "nuclear"
    }
  }
}
output: John Doe is a male person who resides at 123 Main St. He was born on January 1, 1980, making him 44 years old. 
John's annual salary is 80,000. He has been diagnosed with Diabetes and Asthma. In his nuclear family, there are four 
members, and their monthly income is 10,000, with monthly expenses totaling 8,000. There are two occupations in the 
family, and their family indicating a relatively straightforward financial situation.

* Example 02

input: {
  "personalProfile": {
    "name": "Jane Smith",
    "address": "456 Elm St",
    "dob": "1990-02-02",
    "gender": "female",
    "salary": 75000,
    "hiddenDiseases": ["Anxiety"],
    "family": {
      "numMembers": 8,
      "monthlyIncome": 5000,
      "monthlyExpense": 7000,
      "numOccupations": 1,
      "category": "compound"
    }
  }
}
output: Jane Smith is a female individual who lives at 456 Elm St. She was born on February 2, 1990, 
making her 34 years old. Jane earns an annual salary of 75,000. She has been diagnosed with Anxiety. In her compound 
family, there are eight members, with a monthly income of 7,000 and monthly expenses of 5,000. There is only one 
occupation in the family, and they can be faced potential challenges or intricacies in managing their finances due to 
less income per month compared with expenses per month.

* Example 03

input: {
  "personalProfile": {
    "name": "Mike Lee",
    "address": "789 Oak St",
    "dob": "2000-03-03",
    "gender": "male",
    "salary": 60000,
    "hiddenDiseases": [],
    "family": {
      "numMembers": 1,
      "monthlyIncome": 5000,
      "monthlyExpense": 5000,
      "numOccupations": 1,
      "category": "nuclear"
    }
  }
}
output: Mike Lee is a male individual living at 789 Oak St. He was born on March 3, 2000, making him 24 years old. 
Mike's annual salary is 60,000, and he does not have any hidden diseases. In his family, there is only one member, 
with a monthly income and expenses both amounting to 5,000. Mike is the sole occupation in his simplex family, and their 
family indicating a balanced financial situation.
```

```
Here are some examples for personal emotion profile JSON objects for better understanding to follow provided instructions:

* Example 01

input: {
  "emotionalProfile": {
    "mostlyEngagingFacialEmotion": {
      "emotion": "happy",
      "probability": 80,
      "avgArousal": 60.5,
      "avgValence": 92.3
    },
    "mostlyEngagingSentimentalEmotion": {
      "emotion": "neutral",
      "probability": 50,
      "avgArousal": 78.1,
      "avgValence": 98.7
    }
  }
}
output: This person is predominantly positive in their emotional engagement profile, with a highly engaging facial 
emotion of "happy" (80% probability). This emotion reflects very high positivity (92.3 valence) and high arousal (60.5),
indicating joy or excitement. Their engaging sentimental emotion is "neutral" (50% probability) but with extremely 
high positivity (98.7 valence) and very high arousal (78.1), suggesting a mix of positive and neutral sentiments 
leaning towards positivity. Overall, this individual's emotional profile indicates a generally positive outlook.

* Example 02

input: {
  "emotionalProfile": {
    "mostlyEngagingFacialEmotion": {
      "emotion": "anger",
      "avgArousal": 85.2,
      "avgValence": 47.8
    },
    "mostlyEngagingSentimentalEmotion": {
      "emotion": "happy",
      "avgArousal": 72.4,
      "avgValence": 71.9
    }
  }
}
output: 
This person's emotional profile suggests a mix of positivity and negativity. Their most engaging facial emotion is 
"anger" with high arousal (85.2) and moderate positivity (47.8 valence), indicating frustration or irritation. On the 
other hand, their engaging sentimental emotion is "happy" with slightly lower arousal (72.4) but higher positivity 
(71.9 valence), indicating joy or contentment. This combination suggests a complex emotional state, where positivity 
from happiness might counterbalance the negativity from anger.

* Example 03

input: {
  "emotionalProfile": {
    "mostlyEngagingFacialEmotion": {
      "emotion": "sad",
      "accuracy": 73,
      "avgArousal": 38.9,
      "avgValence": 54.1
    },
    "mostlyEngagingSentimentalEmotion": {
      "emotion": "fear",
      "accuracy": 85,
      "avgArousal": 25.7,
      "avgValence": 78.3
    }
  }
}
output: 
This person's emotional profile suggests a predominant engagement with negative emotions. Their most engaging facial 
emotion is "sad" (73% accuracy) with moderate arousal (38.9) and a moderate negative valence (54.1), reflecting feelings
of sadness or melancholy. Furthermore, their engaging sentimental emotion is "fear" (85% accuracy) with low arousal 
(25.7) but a high negative valence (78.3), indicating feelings of anxiety or apprehension. These emotional states may 
impact decision-making processes by influencing risk aversion or cautiousness. Addressing the underlying causes of 
these emotions could be essential for improving the individual's emotional well-being and effectiveness in the 
workplace.
```
Begin!

Input JSON Object: {{ profile }}
'''
PROFILES_INTO_RECOMMENDATION_PROMPT_TEMPLATE = '''
You're a helpful assistant skilled at offering employee recommendations based on thorough analysis of their personal 
bio data and emotional engagement profiles. Your derived recommendation is considered as your final answer.

Here is the personal bio data profile of the employee: {bio_data_profile}

Here is the emotional engagement profile of the employee: {emotion_engagement_profile}

You've received a worker's biodata and emotional engagement profiles. Utilize these to provide insightful 
recommendations for the specific worker/employee. Ensure to consider their strengths, financial stability, and 
emotional disposition. Your answer should be concise and clear, supporting informed decision-making. Employ British 
English accent with passive tense when crafting your response. Limit your response to a maximum of 250 words.

Begin!

Recommendation Answer:
'''
