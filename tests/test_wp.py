from pytest import approx

from happytransformer import HappyWordPrediction, ARGS_WP_TRAIN, ARGS_WP_EVAl
from happytransformer.happy_word_prediction import WordPredictionResult
from tests.shared_tests import run_save_load_train


def test_mwp_basic():
    MODELS = [
        ('DISTILBERT', 'distilbert-base-uncased', 'pepper'),
        ('BERT', 'bert-base-uncased', '.'),
        ('ALBERT', 'albert-base-v2', 'garlic'),
        ('ROBERTA', "roberta-base", "pepper")
    ]
    for model_type, model_name, top_result in MODELS:
        happy_wp = HappyWordPrediction(model_type, model_name)
        results = happy_wp.predict_mask(
            "Please pass the salt and [MASK]",
        )
        result = results[0]
        assert result.token == top_result


def test_mwp_top_k():
    happy_wp = HappyWordPrediction('DISTILBERT', 'distilbert-base-uncased')
    result = happy_wp.predict_mask(
        "Please pass the salt and [MASK]",
        top_k=2
    )
    answer = [
        WordPredictionResult(token='pepper', score=approx(0.2664579749107361, 0.01)),
        WordPredictionResult(token='vinegar', score=approx(0.08760260790586472, 0.01))
    ]

    assert result == answer


def test_mwp_targets():
    happy_wp = HappyWordPrediction('DISTILBERT', 'distilbert-base-uncased')
    result = happy_wp.predict_mask(
        "Please pass the salt and [MASK]",
        targets=["water", "spices"]
    )
    answer = [
        WordPredictionResult(token='water', score=approx(0.014856964349746704, 0.01)),
        WordPredictionResult(token='spices', score=approx(0.009040987119078636, 0.01))
    ]
    assert result == answer

def test_mwp_train_basic():
    happy_wp = HappyWordPrediction('', 'distilroberta-base')
    happy_wp.train("../data/wp/train-eval.txt")

def test_mwp_eval_basic():
    happy_wp = HappyWordPrediction('', 'distilroberta-base')
    result = happy_wp.eval("../data/wp/train-eval.txt")
    assert type(result.loss) == float

def test_mwp_train_effectiveness_multi():
    happy_wp = HappyWordPrediction('', 'distilroberta-base')

    before_result = happy_wp.eval("../data/wp/train-eval.txt")

    happy_wp.train("../data/wp/train-eval.txt")
    after_result = happy_wp.eval("../data/wp/train-eval.txt")

    assert after_result.loss < before_result.loss

def test_mwp_eval_some_settings():
    """
    Test to see what happens when only a subset of the potential settings are used
    :return:
    """
    args = {'line_by_line': True,
            }
    happy_wp = HappyWordPrediction('', 'distilroberta-base')
    result = happy_wp.eval("../data/wp/train-eval.txt", args)
    assert type(result.loss) == float


def test_gen_save_load_train():
    happy_wp = HappyWordPrediction('', 'distilroberta-base')
    output_path = "data/wp-train.txt"
    data_path = "../data/wp/train-eval.txt"
    run_save_load_train(happy_wp, output_path, ARGS_WP_TRAIN, data_path, "train")

def test_gen_save_load_eval():
    happy_wp = HappyWordPrediction('', 'distilroberta-base')
    output_path = "data/wp-eval.txt"
    data_path = "../data/wp/train-eval.txt"
    run_save_load_train(happy_wp, output_path, ARGS_WP_EVAl, data_path, "eval")

def test_wp_save():
    happy = HappyWordPrediction("BERT", "prajjwal1/bert-tiny")
    happy.save("model/")
    result_before = happy.predict_mask("I think therefore I [MASK]")

    happy = HappyWordPrediction(load_path="model/")
    result_after = happy.predict_mask("I think therefore I [MASK]")

    assert result_before[0].token ==result_after[0].token



