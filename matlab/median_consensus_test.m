close all; clear; clc;

%rng(1);

n = 3;
mu = 1;
alpha = 1;
lambda = alpha + mu^2;

dt = 1e-4;
max_t = 5;
A = rand_adj(n);

z = randi(10,[n,1]);
m = ones(n,1) * median(z);

xdot = grad(m,A,n,z,alpha,lambda);
x = m + xdot * dt;
xdot2 = grad(x,A,n,z,alpha,lambda);

n = 3;
z = [10,1,8];
A = [0,1,0;1,0,1;0,1,0];



%%

odefun = @(t,y) grad(y,A,n,z,alpha,lambda);
[t,X] = ode45(odefun,[0,10],z,odeset('MaxStep',1e-3));

figure;
hold on;
plot(t,X(:,1),'linewidth',2);
plot(t,X(:,2),'linewidth',1.5);
plot(t,X(:,3),'linewidth',1);
legend("x_1","x_2","x_3");
xlabel("Time")
ylabel("State")
% plot(t,X,'r','linewidth',1.5)
% yline(median(z),'k--')
% yline(mean(z),'r--')

function [A] = rand_adj(N)
    A = zeros(N,N);
    visited = zeros(N,1);
    i = randi(N);
    visited(i) = 1;
    while ~all(visited)
        j = randi(N);
        while i==j
            j = randi(N);
        end
        A(i,j) = 1; A(j,i) = 1;
        visited(j) = 1;
        i = j;
    end
end

function [xdot] = grad(x,A,n,z,alpha,lambda)
xdot = zeros(n,1);
for i = 1:n
    xdot(i) = - alpha * sign(x(i) - z(i));
    for j = 1:n
        if A(i,j)
            xdot(i) = xdot(i) - lambda * sign(x(i) - x(j));
        end
    end
end
end