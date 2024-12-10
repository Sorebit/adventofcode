#include <bits/stdc++.h>
using namespace std;

#define sim template <class c
#define ris return *this
#define dor > debug &operator<<
#define eni(x)                                                                    \
    sim > typename enable_if<sizeof dud<c>(0) x 1, debug &>::type operator<<(c i) \
    {
sim > struct rge
{
    c b, e;
};
sim > rge<c> range(c i, c j) { return rge<c>{i, j}; }
sim > auto dud(c *x) -> decltype(cerr << *x, 0);
sim > char dud(...);
struct debug
{
#ifdef XOX
    ~debug()
    {
        cerr << endl;
    }
    eni(!=) cerr << boolalpha << i;
    ris;
} eni(==) ris << range(begin(i), end(i));
}
sim, class b dor(pair<b, c> d)
{
    ris << "" << d.first << " --> " << d.second << "";
}
sim dor(rge<c> d)
{
    *this << "[";
    for (auto it = d.b; it != d.e; ++it)
        *this << ", " + 2 * (it == d.b) << *it;
    ris << "]";
}
#else
    sim dor(const c &)
    {
        ris;
    }
#endif
}
;

#define imie(...) "" << #__VA_ARGS__ " = " << (__VA_ARGS__) << ", "
#define f first
#define s second

#define all(x) (x).begin(), (x).end()


const int mod = 1e9 + 7;
const int nax = 1e6 + 9;
int N = 0;
int value[nax];
vector<int> g[nax];
bool opened[nax];
int res = 0;
vector<int>good;
void dfs2(int v, int fuel, int ans)
{
    if(fuel < 0)
        return;
    if(fuel >= 0)
    {
        res = max(res,ans);
        cout << res << endl;
        // return;
    }
    if(fuel == 0)
        return;
    vector<int>path(N+1,-1);
    queue<int>q;
    path[v] = 0;
    q.push(v);
    while(!q.empty())
    {
        int a = q.front();
        q.pop();
        for(int b : g[a])
        {
            if(path[b] == -1)
            {
                path[b] = path[a]+1;
                q.push(b);
            }
        }
    }   
    for(int i : good)
    {
        if(path[i] != -1 && opened[i] == false && value[i] != 0)
        {
            opened[i] = true;
            fuel -= path[i];
            fuel--;
            ans += (fuel*value[i]);
            dfs2(i,fuel,ans);
            opened[i] = false;
            ans -= (fuel*value[i]);
            fuel += path[i];
            fuel++;
        }
    }
}
void dfs(int v, int fuel, int ans)
{
    if(fuel < 0)
        return;
    if(fuel >= 0)
    {
        dfs2(0,26,ans);
        // res = max(res,ans);
        // cout << ans << endl;
    }
    if(fuel == 0)
        return;
    vector<int>path(N+1,-1);
    queue<int>q;
    path[v] = 0;
    q.push(v);
    while(!q.empty())
    {
        int a = q.front();
        q.pop();
        for(int b : g[a])
        {
            if(path[b] == -1)
            {
                path[b] = path[a]+1;
                q.push(b);
            }
        }
    }   
    for(int i : good)
    {
        if(path[i] != -1 && opened[i] == false && value[i] != 0)
        {
            opened[i] = true;
            fuel -= path[i];
            fuel--;
            ans += (fuel*value[i]);
            dfs(i,fuel,ans);
            opened[i] = false;
            ans -= (fuel*value[i]);
            fuel += path[i];
            fuel++;
        }
    }
}
int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie();
    int a,n,b,ile;
    cin >> ile;     
    for(int i = 1;i<=ile;i++)
    {
        cin >> a >> value[a] >> n;
        if(value[a] != 0)
            good.push_back(a);
        N = max(N,a);
        while(n--)
        {
            cin >> b;
            g[a].push_back(b);
        }
    }
    random_shuffle(all(good));
    // dfs(0,26,0);
    vector<int>v;
    for(int i = 0;i<5;i++)
        v.push_back(i);
    debug() << imie(v);
    // cout << res;
}
