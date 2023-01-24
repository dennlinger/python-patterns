"""
This pattern uses a specific tokenizer over a whitesplit approximation, and compares the runtime efficiency of both.
"""
import time

from allennlp.predictors.predictor import Predictor

if __name__ == '__main__':
    sample = {'article': "By . Ray Massey, Transport Editor . PUBLISHED: . 19:31 EST, 19 September 2013 . | . UPDATED: . 19:32 EST, 19 September 2013 . The number of parking tickets issued on a Sunday has rocketed after scores of councils introduced seven-day patrols. Figures show motorists are being stung by almost 900,000 parking fines a month at a cost of £30million – a 4 per cent rise on the previous year. And tickets issued on Sundays have increased by 13 per cent – with nearly 300,000 tickets issued on that day of the week in the first five months of 2013. Increase: Motorists are being stung by almost 900,000 parking fines a month at a cost of £30million - a 4 per cent rise on the previous year. While tickets issued on Sundays have increased by 13 per cent . It is believed the rise of Sunday shopping has prompted more town halls to crack down on parking on a day when rules were traditionally relaxed. And the AA says some traffic wardens had even ‘targeted churchgoers and choristers’. The figures were revealed by LV= car insurance in a series of freedom of information requests. The AA says some traffic wardens had even 'targeted churchgoers and choristers' The company said: ‘While there has been\xa0 a general increase across all council areas, there has been\xa0 a significant spike in the number of tickets being issued on Sundays.’ Westminster Council in London has given out the largest number of Sunday parking tickets so far this year at 16,464, followed by the London borough of Lambeth (6,590), Birmingham City Council (3,909), the London borough of Bexley (3,786) and Bristol (1,686). Councils across the UK now hand out an average of 162 parking tickets a day, compared to 154 in 2012, according to the LV= report. But drivers suffer a postcode lottery when it comes to rules on Sunday parking. John O’Roarke, managing\xa0 director of LV=, said: ‘Parking on a Sunday is becoming increasingly difficult and it’s easy to get caught out if you don’t know the local rules.’ AA president Edmund King said it was ‘as if nothing is sacred’, adding: ‘It’s mean-spirited to fine people on a Sunday. ‘The traditional day of rest – when even motorists deserve a bit of relief – is being eroded\xa0 in favour of revenue raising. Money destined for the collection plate is instead flowing into council coffers.’",
              'highlights': "Motorists are being handed nearly 900,000 parking fines a month .\nTickets issued on Sundays have increased by 13 per cent .\nThe AA says some traffic wardens 'target churchgoers and choristers'",
              'id': 'e32de69bba488379354ecb86d67deb46d7b4cc3a'}

    srl_model = Predictor.from_path(
        "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz",
        # cuda_device=0,
    )

    start = time.time()
    for _ in range(100):
        res = srl_model._dataset_reader.bert_tokenizer.tokenize(sample["article"])
    end = time.time()

    print(f"100 iterations with tokenizer took {(end - start):.6f} s.")

    start = time.time()
    for _ in range(100):
        res = sample["article"].split(" ")
    end = time.time()
    print(f"100 iterations with whitesplit approximation took {(end - start):.4f} s.")