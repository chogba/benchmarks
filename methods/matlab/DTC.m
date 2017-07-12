% @file DECISIONTREE.m
%
% DECISION TREE with matlab.

function dtc(cmd)
% This program trains the Decision Tree classifier on the given labeled
% training set and then uses the trained classifier to classify the points
% in the given test set. Labels are expected to be the last row of the
% training set.
%
% Required options:
%     (-T) [string]    A file containing the test set.
%     (-t) [string]    A file containing the training set.

trainFile = regexp(cmd, '.*?-t ([^\s]+)', 'tokens', 'once');
testFile = regexp(cmd, '.*?-T ([^\s]+)', 'tokens', 'once');

% Load input dataset.
TrainData = csvread(trainFile{:});
TestData = csvread(testFile{:});

% Use the last row of the training data as the labels.
labels = TrainData(:,end);
% Remove the label row.
TrainData = TrainData(:,1:end-1);

% Create and train the classifier.
total_time = tic;
classifier = fitctree(TrainData, labels);
% Run Decision Classifier on the test dataset.
labels = predict(classifier, TestData);
% Save prediction of each class for test data.
csvwrite('predictions.csv', labels);

end
