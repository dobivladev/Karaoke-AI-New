from model_training.training import main

learning_rate = 5e-4
batch_size = 20
epochs = 10
libri_train_set = "train-clean-100"
libri_test_set = "test-clean"
comet_api_key = "CDWzFQH0KU3sATx1JCWQvDgbN"

main(learning_rate, batch_size, epochs, libri_train_set, libri_test_set, comet_api_key)