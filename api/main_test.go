package main

import (
	"net/http"
	"net/url"
	"testing"

	"github.com/jmoiron/sqlx"
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
			want: baseQuery + " WHERE \"Team\" LIKE 'NYY' ;",
		},
		{
			name: "single WHERE condition (Name)",
			args: args{
				startingString: baseQuery,
				values: url.Values{
					"Name": []string{"Barry-Bonds"},
				},
			},
			want: baseQuery + " WHERE \"Name\" LIKE 'Barry Bonds' ;",
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

func TestOpenConnection(t *testing.T) {
	tests := []struct {
		name string
		want *sqlx.DB
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := OpenConnection(); got != tt.want {
				t.Errorf("OpenConnection() = %v, want %v", got, tt.want)
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
