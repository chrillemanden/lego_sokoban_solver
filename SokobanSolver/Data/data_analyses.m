clear 
close all
clc

P = '.';
S = dir(fullfile(P,'*.csv')); 
for k = 1:numel(S)
    F = fullfile(P,S(k).name);
    S(k).data = csvread(F);
end

for i = 61:9
    
    fprintf('Test number %.f: Memory = %.4f Time = %.4f Length = %.f\n', i, mean(S(i).data(:,4))/1000, mean(S(i).data(:,2)),mean(S(i).data(:,3)))
    
end