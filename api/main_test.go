package main

import (
	"net/http"
	"net/url"
	"testing"

	_ "github.com/lib/pq"
)

func Test_qstringBuilder(t *testing.T) {
	baseQuery := "SELECT \"Season\", \"Name\", \"Team\" FROM batting_data" // Using shorter query for readability
	type args struct {
		startingString string
		values         url.Values
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{
			name: "no filter parameters",
			args: args{
				startingString: baseQuery,
				values:         url.Values{},
			},
			want: baseQuery + " LIMIT 2;",
		},
		{
			name: "single WHERE condition (Team)",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Team": []string{"NYY"},
				},
			},
			want: baseQuery + " WHERE \"Team\" LIKE 'NYY';",
		},
		{
			name: "single WHERE condition (Name)",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Name": []string{"Barry-Bonds"},
				},
			},
			want: baseQuery + " WHERE \"Name\" LIKE 'Barry Bonds';",
		},
		{
			name: "single WHERE condition (Single Season)",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Season": []string{"2002"},
				},
			},
			want: baseQuery + " WHERE \"Season\" = 2002;",
		},
		{
			name: "Multiple WHERE condition (Season Range) 1",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Season": []string{"2002", "2020"},
				},
			},
			want: baseQuery + " WHERE \"Season\" >= 2002 AND \"Season\" <= 2020;",
		},
		{
			name: "Multiple WHERE condition (Season Range) 2",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Season": []string{"2014", "2000"},
				},
			},
			want: baseQuery + " WHERE \"Season\" >= 2000 AND \"Season\" <= 2014;",
		},
		{
			name: "Multiple WHERE condition (Team + Season)",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Team":   []string{"NYY"},
					"Season": []string{"2002"},
				},
			},
			want: baseQuery + " WHERE \"Season\" = 2002 AND \"Team\" LIKE 'NYY';",
		},
		{
			name: "Multiple WHERE condition (Name + Season)",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Season": []string{"2021"},
					"Name":   []string{"Max-Scherzer"},
				},
			},
			want: baseQuery + " WHERE \"Name\" LIKE 'Max Scherzer' AND \"Season\" = 2021;",
		},
		{
			name: "Multiple WHERE condition (Team + Season)",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Season": []string{"2009"},
					"Team":   []string{"LAD"},
				},
			},
			want: baseQuery + " WHERE \"Season\" = 2009 AND \"Team\" LIKE 'LAD';",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := qstringBuilder(tt.args.startingString, tt.args.values); got != tt.want {
				t.Errorf("qstringBuilder() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestBatterGetHandler(t *testing.T) {
	type args struct {
		w http.ResponseWriter
		r *http.Request
	}
	tests := []struct {
		name string
		args args
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			BatterGetHandler(tt.args.w, tt.args.r)
		})
	}
}

func TestPitcherGetHandler(t *testing.T) {
	type args struct {
		w http.ResponseWriter
		r *http.Request
	}
	tests := []struct {
		name string
		args args
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			PitcherGetHandler(tt.args.w, tt.args.r)
		})
	}
}
