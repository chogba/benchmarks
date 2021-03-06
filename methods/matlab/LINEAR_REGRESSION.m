% @file LINEAR_REGRESSION.m
% @author Marcus Edel
%
% Linear Regression with matlab.

function linear_regression(cmd)
% Simple Linear Regression Prediction.
%
% Required options:
%     (-i) [string]    File containing X (regressors).
%
% Options:
%     (-r) [string]    File containing y (responses). If not given, the
%                      responses are assumed to be the last row of the
%                      input file.
%     (-t) [string]    File containing the test instnces.

% Load input dataset.
regressorsFile = regexp(cmd, '.*?-i ([^\s]+)', 'tokens', 'once');
responsesFile = regexp(cmd, '.*?-r ([^\s]+)', 'tokens', 'once');
testFile = regexp(cmd, '.*?-t ([^\s]+)', 'tokens', 'once');

X = csvread(regressorsFile{:});

if isempty(responsesFile)
  y = X(:,end);
  X = X(:,1:end-1);
else
  y = csvread(responsesFile{:});
end

% Perform linear regression.
total_time = tic;
B = fitlm(X, y);

if ~isempty(testFile)
    % Predicted the classes.
    testSet = csvread(testFile{:});
    predictions = predict(B, testSet);
    % Map the probabilities to the actual classes.
    [~, idx] = max(predictions, [], 2);
end

total_time = tic;
disp(sprintf('[INFO ]   total_time: %fs', toc(total_time)))

if ~isempty(testFile)
    csvwrite('predictions_matlab_linear.csv', idx);
    csvwrite('matlab_linear_probs.csv', predictions);
end

end
